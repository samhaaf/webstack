
import argparse
import os, subprocess
import json
import boto3, botocore
import re
from pprint import pprint
import time
from datetime import datetime


## Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('--stage', '-s', type=str, default=None)
args = parser.parse_args()


 # assert stage argument
assert args.stage is not None, '--stage argument expected'


## Load config
local_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(f"{local_dir}/../../config/")
process = subprocess.run(
    ['make','print', f'stage={args.stage}'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
if process.stderr:
    raise RuntimeError(f'In config/bin/generate.py:\n\n{process.stderr.decode()}')
try:
    config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')))
except json.decoder.JSONDecodeError:
    config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')[1:-1]))


## set tags
tags = [
    {
        'Key': 'stage',
        'Value': args.stage,
    },{
        'Key': 'namespace',
        'Value': config['project']['namespace']
    }
]


## load db build info
with open(f'{local_dir}/../../db/.build/{args.stage}.json') as f:
    db_build_info = json.load(f)


### IAM
iam = boto3.client('iam')
role_name = f"api-{config['project']['namespace']}-{args.stage}"
policies = [
    {"name": "CloudWatchLogsFullAccess"},
    {"arn": db_build_info['iam_ruser']['policy']['Arn']},
    {"arn": db_build_info['iam_rwuser']['policy']['Arn']},
    {"arn": db_build_info['iam_admin']['policy']['Arn']},
    {
        "make": True,
        "name": f"{role_name}-custom",
        "policy_document": {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "rds:DescribeDBInstances"
                ],
                "Resource": [
                    # f"{resource_arn}/{iam_user_name}"
                    "*"
                ]
            }]
        }
    }
]


## get all policies
all_policies = []
pagination_token = None
while True:
    if pagination_token is None:
        response = iam.list_policies(
            Scope='All'
        )
    else:
        response = iam.list_policies(
            Scope='All',
            Marker=pagination_token
        )
    all_policies += response['Policies']
    pagination_token = response.get('Marker')
    if not pagination_token:
        break


# pprint([p['PolicyName'] for p in sorted(all_policies, key=lambda k: k['PolicyName'])])

## Get policy arns, if they exist
for p in range(len(policies)):
    if 'arn' not in policies[p]:
        found = False
        for _policy in all_policies:
            if _policy['PolicyName'] == policies[p]['name']:
                policies[p]['arn'] = _policy['Arn']
                found = True
                break
        if not found:
            if policies[p].get('make'):
                print('Creating Policy:', policies[p]['name'])
                response = iam.create_policy(
                    PolicyName = policies[p]['name'],
                    PolicyDocument = json.dumps(policies[p]['policy_document']),
                    Description='A custom policy for a webstack deployment',
                )
                policies[p]['arn'] = response['Policy']['Arn']
            else:
                print('Policy not found with name:', policies[p]['name'])


## check for role
try:
    response = iam.get_role(RoleName=role_name)
    role = response['Role']
    print('Role found:', role_name)


## if it does not exist, create it
except iam.exceptions.NoSuchEntityException:
    print('Creating role:', role_name)
    response = iam.create_role(
        RoleName = role_name,
        AssumeRolePolicyDocument = json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "Service": ["lambda.amazonaws.com"]
                },
                "Action": [
                    "sts:AssumeRole"
                ]
            }]
        }),
        Description = 'A role to access RDS resources',
        Tags = tags
    )
    role = response['Role']


## Attach Policies to Role:
for policy in policies:
    print('Attaching Policy to Role:', policy['arn'])
    response = iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy['arn']
    )



def serialize(node):
    if isinstance(node, dict):
        return { key: serialize(value) for key, value in node.items() }
    if isinstance(node, list):
        return [serialize(value) for value in node]
    if isinstance(node, datetime):
        return node.strftime("%m/%d/%Y, %H:%M:%S")
    return node


## write build info for the API
with open(f'{local_dir}/../.build/{args.stage}.json', 'w') as f:
    json.dump({
        'iam_role': serialize(role)
    }, f)
