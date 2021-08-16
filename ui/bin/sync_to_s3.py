import boto3, botocore
import subprocess
import json
import hjson
import os
import argparse
import time
import copy
import logging
from pprint import pprint
import time

logger = logging.getLogger(__name__)


def list_dir_recur(path):
    if not os.path.isdir(path):
        return [path]
    return sum([list_dir_recur(os.path.join(path, p)) for p in os.listdir(path)], [])


def deep_update(dict_1, dict_2):
    assert isinstance(dict_1, dict) and isinstance(dict_2, dict), (
        "assimilate only works on dict types"
    )
    for key in dict_2:
        if not isinstance(dict_1.get(key), dict) or not isinstance(dict_2[key], dict):
            dict_1[key] = dict_2[key]
        else:
            deep_update(dict_1[key], dict_2[key])
    return dict_1


## local dir
local_dir = os.path.dirname(os.path.realpath(__file__))


## Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('--stage', '-s', type=str, default=None)
args = parser.parse_args()

 # assert that a stage has been offerred
assert args.stage is not None, '--stage argument expected'


## Build and load the config from the config module
os.chdir(f"{local_dir}/../../config/")
process = subprocess.run(
    ['make','print', f'stage={args.stage}'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
if process.stderr:
    raise RuntimeError(f'In config/bin/generate.py:\n\n{process.stderr.decode()}')
config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')[1:-1]))


## enter UI root dir
os.chdir(f'{local_dir}/../')


## load s3.lock.json
lock = {"files": {args.stage: {}}}
if os.path.exists('.lock.json'):
    with open('.lock.json') as f:
        lock = json.load(f)


## load s3_config
 # :TODO: update this file at some point with better inclusion/exclusion syntax
with open('s3_config.json') as f:
    s3_config = hjson.load(f)


## Build config for each file. In the case of multiple configs present for a
##   single file, top-down directory inheritance is maintained.
agg_blobs = {}
config_blobs = [blob for blob in s3_config['files']]
while config_blobs:

    # select first blob
    blob = config_blobs[0]
    config_blobs = config_blobs[1:]

    # directory targets have contents enumerated with inherited parameters
    if os.path.isdir(blob['path']):
        path_split = blob['path'].split('/')
        path_depth = len(path_split)
        path_depth -= sum(_ in ['', '.'] for _ in path_split) # ignore current dir
        path_depth -= 2 * sum(_ == '..' for _ in path_split) # decrement for parent dir
        config_blobs += [{
                'path': os.path.join(blob['path'], path),
                'parents': {
                    **blob.get('parents', {}),
                    path_depth: blob
                }
            } for path in os.listdir(blob['path'])]
        continue

    # if there has been no blob for this path, set
    if blob['path'] not in agg_blobs:
        agg_blobs[blob['path']] = blob
        continue

    agg_blob = agg_blobs[blob['path']]
    agg_blob.setdefault('parents', {})

    # make sure there aren't multiple configurations for the same parent file
    if 'parents' in blob:
        duplicate_blobs = [b for k,b in blob['parents'].items() if k in agg_blob['parents']]
        assert not any(duplicate_blobs), (
            f'Duplicate configuration found for path(s): {[b["path"] for b in duplicate_blobs]}'
        )

    # join this blob with the aggregate
    deep_update(agg_blob, blob)


## Determine which files to upload
to_upload = []
for path, agg_blob in agg_blobs.items():
    upload = False

    # build consolidated config for file
    file_blob = {}
    for depth in sorted(agg_blob['parents']):
        parent = agg_blob['parents'][depth]
        file_blob.update({
            k: v for k,v in parent.items() if k not in ['path', 'parents']
        })
    del agg_blob['parents']
    file_blob.update(agg_blob)


    # if the file_blob says to ignore, continue
    if file_blob.get('ignore'):
        continue

    # extra upload arguments
    file_blob['boto3_args'] = {}
    if path[-4:] == '.css' and config.get('auto_css', True):
        file_blob['boto3_args']['ContentType'] = "text/css"
    if file_blob.get('serve_html'):
        file_blob['boto3_args']['ContentType'] = "text/html"

    # get last file modified time
    modified_time = os.path.getmtime(path)

    lock_blob = lock['files'][args.stage].setdefault(file_blob['path'], {})

    # if no record in lock file, we know to upload
    if not lock_blob:
        upload = True

    # if the file was modified since last upload, upload
    if modified_time > lock_blob.get('upload_time', 0):
        upload = True

    # if the boto3_args on a file have changed since last upload, upload
    if file_blob['boto3_args'] != lock_blob.get('boto3_args'):
        upload = True

    # if we have determined to upload this file
    if upload:
        to_upload.append(file_blob)
        lock_blob['upload_time'] = time.time()
        lock_blob['boto3_args'] = file_blob['boto3_args']


## TODO: generate access policy
 # TODO: update policy and policy update time in lock file


## start s3 service
s3 = boto3.client('s3')


## TODO: update access policy in s3, if applicable


## push each updated file to the bucket in config['aws']['s3_bucket']
invalidation_paths = []
print('Pushing files to AWS Bucket:', config['aws']['s3_bucket'])
for file_blob in to_upload:

    invalidation_paths.append('/' + '/'.join(file_blob['path'].split('/')[1:]))

    key = os.path.join(args.stage, file_blob['path'])

    if config['aws'].get('root_path'):
        key = f'{config["aws"]["root_path"]}/{key}'

    print(f'..{key}')
    with open(file_blob["path"], 'rb') as f:
        response = s3.put_object(
            Bucket = config['aws']['s3_bucket'],
            Key = key,
            Body = f,
            **file_blob['boto3_args']
        )
    if not response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logger.error(f'Failed to upload file_blob: {key}')
        print(response)



## CloudFront
cloudfront = boto3.client('cloudfront')


## create list of distributions
distributions = []
pagination_token = None
while True:
    if pagination_token:
        response = cloudfront.list_distributions(Marker=pagination_token)
    else:
        response = cloudfront.list_distributions()
    if len(response['DistributionList']['Items']) == 0:
        bread
    distributions += response['DistributionList']['Items']
    pagination_token = response['DistributionList'].get('NextMarker')
    if not pagination_token:
        break


## Check for matching cloudfront distribution
distribution = None
for dist in distributions:
    if config['ui']['domain'] in dist['Aliases']['Items']:
        distribution = dist
        print('CloudFront Distribution found:', distribution['Id'])


## send Distribution invalidation for updated files, if there is one
if distribution is not None:
    caller_reference = str(time.time())
    print('Sending Distribution Invalidation:', caller_reference)
    response = cloudfront.create_invalidation(
        DistributionId=distribution['Id'],
        InvalidationBatch={
            'Paths': {
                'Quantity': len(to_upload),
                'Items': invalidation_paths
            },
            'CallerReference': caller_reference
        }
    )
    # print(response)

## persist changes in .lock.json
with open('.lock.json', 'w') as f:
    json.dump(lock, f, indent=4)
