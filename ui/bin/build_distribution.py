"""
Generates an ACM certificate in AWS and validates with a Google Domain.
"""


import argparse
import os, subprocess
import json
import boto3, botocore
import re
from pprint import pprint
import time


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



## S3 Bucket
s3 = boto3.client('s3')

# check if S3 Bucket exists
try:
    s3.head_bucket(Bucket=config['aws']['s3_bucket'])
    print('S3 Bucket found:', config['aws']['s3_bucket'])

# if Bucket does not exist: build
except botocore.exceptions.ClientError as e:
    extra_args = {}
    if config['aws']['region'] != 'us-east-1':
        extra_args['LocationConstraint'] = config['aws']['region']
        response = s3.create_bucket(
            ACL='private',
            Bucket=config['aws']['s3_bucket'],
            **extra_args
        )
        print('Created S3 Bucket:', config['aws']['s3_bucket'])



## ACM Certificate
acm = boto3.client('acm')
domain_name = config['ui']['domain']
# domain_name = 'webstack.haaftools.com'
root_domain = '.'.join(domain_name.split('.')[-2:])

 # automatically process as a www. subdomain for root domain requests
if domain_name == root_domain:
    domain_name = f'www.{root_domain}'

 # retrieve list of all certificates
pagination_token = None
certificates = []
while True:
    if pagination_token:
        response = acm.list_certificates(NextToken=pagination_token)
    else:
        response = acm.list_certificates()
    certificates += response['CertificateSummaryList']
    if not response.get('NextToken'):
        break
    pagination_token = response['NextToken']

 # find the certificate that supports requested domain name, if it exists
certificate = None
for cert in [cert for cert in certificates if cert['DomainName'] == root_domain]:
    response = acm.describe_certificate(CertificateArn=cert['CertificateArn'])

     # if there is a direct match for the subdomain: mark as match
    if domain_name in response['Certificate']['SubjectAlternativeNames']:
        certificate = response['Certificate']

     # if there is a length(3) wildcard subdomain: mark as match
    if len(domain_name.split('.')) == 3:
        if f'*.{root_domain}' in response['Certificate']['SubjectAlternativeNames']:
            certificate = response['Certificate']

     # if domain_name is length(4) and there is a length(4) wildcard subdomain: mark as match
    if len(domain_name.split('.')) == 4:
        wildcard_name = f'*.{".".join(domain_name.split(".")[-3:])}'
        if wildcard_name in response['Certificate']['SubjectAlternativeNames']:
            certificate = response['Certificate']

    print(f'ACM Certificate found matching: {root_domain} & *.{root_domain}')

 # if there was no matching certificate: request one
if certificate is None:
    response = acm.request_certificate(
        DomainName=root_domain,
        ValidationMethod='DNS',
        IdempotencyToken=f"wildcard_{re.sub(root_domain, '.', '_')}",
        SubjectAlternativeNames=[
            f'*.{root_domain}',
            domain_name,
        ]
    )
    certificate = acm.describe_certificate(CertificateArn=response['CertificateArn'])['Certificate']
    print(f'ACM Certificate requested for domains: {root_domain} & *.{root_domain}')

 # Output certificate status
print(f'Certificate status:', certificate['Status'])

 # if the certificate is pending validation: tell user to add CNAME to DNS record
add_cname_records = None
if certificate['Status'] == 'PENDING_VALIDATION':
    add_cname_records = []
    unique_set = set()
    for item in certificate['DomainValidationOptions']:
        if item['ResourceRecord']['Name'] in unique_set:
            continue
        unique_set.add(item['ResourceRecord']['Name'])
        add_cname_records.append(item['ResourceRecord'])
    print('Two CNAME entries need to be added to the DNS record:')
    for record in add_cname_records:
        print('... Name:', record['Name'])
        print('    Value:', record['Value'])



## Route53
route53 = boto3.client('route53')

 # Get list of all hosted zones
pagination_token = None
hosted_zones = []
while True:
    if pagination_token:
        response = route53.list_hosted_zones(Marker=pagination_token)
    else:
        response = route53.list_hosted_zones()
    hosted_zones += response['HostedZones']
    if not response.get('NextMarker'):
        break
    pagination_token = response['NextMarker']

 # Find matching Hosted Zone
hosted_zone = None
for zone in hosted_zones:
    if zone['Name'] == f'{root_domain}.':
        hosted_zone = zone
        print(f'Route53 Hosted Zone found matching Name={root_domain}.')

 # If Hosted Zone does not exist: create it
if hosted_zone is None:
    caller_reference = str(time.time())
    response = route53.create_hosted_zone(
        Name=f'{root_domain}.',
        CallerReference=caller_reference,
    )
    print('Created Route53 Hosted Zone with caller reference:', caller_reference)
    hosted_zone = response['HostedZone']

 # Get Hosted Zone records
hosted_zone_records = []
while True:
    if len(hosted_zone_records):
        response = route53.list_resource_record_sets(
            HostedZoneId=hosted_zone['Id'],
            StartRecordName=hosted_zone_records[-1]['Name'] + 'Z',
        )
    else:
        response = route53.list_resource_record_sets(
            HostedZoneId=hosted_zone['Id'],
        )
    if not len(response['ResourceRecordSets']):
        break
    hosted_zone_records += response['ResourceRecordSets']

 # Get the NS record set
ns_record_set = None
for record in hosted_zone_records:
    if record['Type'] == 'NS':
        ns_record_set = record

 # assert that there is an ns_record_set
assert ns_record_set, 'No NS record set found. Human inspection required.'

 # Print Name Server values
print('Make sure your DNS configuration routes to these Namespace Servers:')
for value in ns_record_set['ResourceRecords']:
    print(f"... {value['Value'][:-1]}")

 # Upsert CNAME records
for record in add_cname_records or []:
    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone['Id'],
        ChangeBatch={
            'Comment': f'Upserted {time.time()}',
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': record['Name'],
                    'Type': 'CNAME',
                    'ResourceRecords': [{'Value': record['Value']}],
                    "TTL": 300
                }
            }]
        }
    )
print('Upserted CNAME records into Route53 Hosted Zone')



##  CloudFront Origin Access Identity
cloudfront = boto3.client('cloudfront')

 # build list of all identities
identities = []
pagination_token = None
while True:
    if pagination_token:
        response = cloudfront.list_cloud_front_origin_access_identities(
            Marker=pagination_token
        )['CloudFrontOriginAccessIdentityList']
    else:
        response = cloudfront.list_cloud_front_origin_access_identities(
        )['CloudFrontOriginAccessIdentityList']
    identities += response.get('Items', [])
    if len(response.get('Items', [])) == 0 or not response.get('NextMarker'):
        break

 # check for a matching identity from the list of identities
origin_access_identity = None
for identity in identities:
    if identity['Comment'] == config['aws']['s3_bucket']:
        origin_access_identity = identity
        print('CloudFront Origin Access Identity found:', identity['Id'])

 # If no match found, create an origin access identity
if origin_access_identity is None:
    response = cloudfront.create_cloud_front_origin_access_identity(
        CloudFrontOriginAccessIdentityConfig={
            'CallerReference': config['aws']['s3_bucket'],
            'Comment': config['aws']['s3_bucket'],
        }
    )
    origin_access_identity = response['CloudFrontOriginAccessIdentity']
    print(f'Created CloudFront Origin Access Identity: {origin_access_identity}')



## Cloudfront Distribution

 # create list of distributions
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

 # Check for existing cloudfront distribution
distribution = None
for dist in distributions:
    if domain_name in dist['Aliases']['Items']:
        distribution = dist
        print('CloudFront Distribution found:', distribution['Id'])

 # If no distribution was found: create one
if distribution is None:

     # Create the distribution
    s3_path = f'/{args.stage}/public'
    response = cloudfront.create_distribution_with_tags(
        DistributionConfigWithTags={
            'DistributionConfig': {
                'CallerReference': domain_name,
                'Aliases': {
                    'Quantity': 1,
                    'Items': [domain_name]
                },
                'DefaultRootObject': 'index.html',
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': f'S3-{config["aws"]["s3_bucket"]}{s3_path}',
                        'DomainName': f'{config["aws"]["s3_bucket"]}.s3.amazonaws.com',
                        'OriginPath': s3_path,
                        'CustomHeaders': {
                            'Quantity': 1,
                            'Items': [{
                                'HeaderName': 'stage',
                                'HeaderValue': args.stage,
                            }]
                        },
                        'S3OriginConfig': {
                            'OriginAccessIdentity': f'origin-access-identity/cloudfront/{origin_access_identity["Id"]}',
                        },
                    }]
                },
                'OriginGroups': {'Quantity': 0},
                'DefaultCacheBehavior': {
                    'TargetOriginId': f'S3-{config["aws"]["s3_bucket"]}{s3_path}',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'TrustedKeyGroups': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'AllowedMethods': {
                        'Quantity': 2,
                        'Items': ['GET', 'HEAD']
                    },
                    'SmoothStreaming': False,
                    'Compress': True,
                    'LambdaFunctionAssociations': {
                        'Quantity': 0
                    },
                    'FieldLevelEncryptionId': '',
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {'Forward': 'none'},
                        'Headers': {'Quantity': 0},
                        'QueryStringCacheKeys': {'Quantity': 0}
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 300,
                    'MaxTTL': 300
                },
                'CacheBehaviors': {
                    'Quantity': 0
                },
                'CustomErrorResponses': {
                    'Quantity': 1,
                    'Items': [
                        {
                            'ErrorCode': 403,
                            'ResponsePagePath': '/index.html',
                            'ResponseCode': '200',
                            'ErrorCachingMinTTL': 0
                        },
                    ]
                },
                'Comment': '',
                # 'Logging': {
                #     'Enabled': True|False,
                #     'IncludeCookies': True|False,
                #     'Bucket': 'string',
                #     'Prefix': 'string'
                # },
                'PriceClass': 'PriceClass_All',
                'Enabled': True,
                'ViewerCertificate': {
                    'ACMCertificateArn': certificate['CertificateArn'],
                    'SSLSupportMethod': 'sni-only',
                    'MinimumProtocolVersion': 'TLSv1.2_2019',
                    'Certificate': certificate['CertificateArn'],
                    'CertificateSource': 'acm'
                },
                'Restrictions': {
                    'GeoRestriction': {
                        'RestrictionType': 'none',
                        'Quantity': 0,
                    }
                },
                'WebACLId': '',
                'HttpVersion': 'http2',
                'IsIPV6Enabled': True
            },
            'Tags': {
                'Items': [{
                        'Key': 'stage',
                        'Value': args.stage,
                    },{
                        'Key': 'namespace',
                        'Value': config['project']['namespace']
                    }
                ]
            }
        }
    )
    distribution = response['Distribution']
    print(f'Created Distribution: {distribution["Id"]}')



## Update S3 bucket to be accessible by the Distribution
response = s3.put_bucket_policy(
    Bucket=config['aws']['s3_bucket'],
    ConfirmRemoveSelfBucketAccess=False,
    Policy=json.dumps({
        "Version": "2008-10-17",
        "Id": "PolicyForCloudFrontPrivateContent",
        "Statement": [
            {
                "Sid": "1",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {origin_access_identity['Id']}"
                },
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{config['aws']['s3_bucket']}/*/public/*"
            }
        ]
    }),
)
print('Updated S3 Bucket policy')



print(hosted_zone['Id'])
response = route53.change_resource_record_sets(
    HostedZoneId=hosted_zone['Id'],
    ChangeBatch={
        'Comment': f'Upserted {time.time()}',
        'Changes': [{
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': domain_name,
                'Type': 'A',
                'AliasTarget': {
                    'HostedZoneId': "Z2FDTNDATAQYW2",
                    'DNSName': distribution['DomainName'],
                    'EvaluateTargetHealth': True
                },
            }
        }]
    }
)
print('Upserted A record for Distribution into Route53 Hosted Zone')
