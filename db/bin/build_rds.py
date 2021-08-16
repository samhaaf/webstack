
import argparse
import os, subprocess
import json
import boto3, botocore
import re
from pprint import pprint
import time
from sql_utils import execute
import psycopg2
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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



### RDS
rds = boto3.client('rds')


## get instance if it exists
try:
    response = rds.describe_db_instances(DBInstanceIdentifier=config['database']['identifier'])
    instance = response['DBInstances'][0]
    print('Instance found:', config['database']['identifier'])


except rds.exceptions.DBInstanceNotFoundFault:
    instance = None


## if it doesn't exist, create it
if instance == None:
    print('Creating instance:', config['database']['identifier'])

    params = dict(
        DBName = config['database']['name'],
        DBInstanceIdentifier = config['database']['identifier'],
        AllocatedStorage = 20,
        MasterUsername = config['database']['master_username'],
        MasterUserPassword = config['database']['master_password'],
        Tags = tags,
        EnableIAMDatabaseAuthentication=True,
        # EnableCloudwatchLogsExports=[
        #     'postgresql', 'upgrade'
        # ],
    )
    if config['database']['engine'] == 'postgres':
        params.update(dict(
            DBInstanceClass = "db.t2.micro",
            Engine = "postgres",
            # StorageEncrypted=True,
            CopyTagsToSnapshot=True,
        ))
    else:
        raise NotImplementedError(
            f'build for engine={config["database"]["engine"]} not defined'
        )

    response = rds.create_db_instance(**params)
    instance = response['DBInstance']


## connect to database
connection = psycopg2.connect(
    host = instance['Endpoint']['Address'],
    port = instance['Endpoint']['Port'],
    # dbname = config['database']['name'],
    user = config['database']['master_username'],
    password = config['database']['master_password'],
    connect_timeout = 3
)


## step needed to create databases on the instance; unknown function
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);


## use the connection
try:

    ## create the database if it does not exist
    results = execute(connection, f"""
        SELECT 1 FROM pg_database WHERE datname = '{config["database"]["name"]}'
    """)
    if not results:
        print('Creating database:', config['database']['name'])
        results = execute(connection, f"""
            CREATE DATABASE {config['database']['name']}
        """)


    ##  create the read-only user role if not exists
    results = execute(connection, f"""
        SELECT 1 FROM pg_roles WHERE rolname='{config['database']['iam_ruser']}'
    """)
    if not results:
        print('Creating IAM read-only user:', config['database']['iam_ruser'])
        results = execute(connection, f"""
            CREATE USER {config['database']['iam_ruser']} WITH LOGIN;
            GRANT rds_iam TO {config['database']['iam_ruser']};
        """)


    ## create the read-write user role if not exists
    results = execute(connection, f"""
        SELECT 1 FROM pg_roles WHERE rolname='{config['database']['iam_rwuser']}'
    """)
    if not results:
        print('Creating IAM read-write user:', config['database']['iam_rwuser'])
        results = execute(connection, f"""
            CREATE USER {config['database']['iam_rwuser']} WITH LOGIN;
            GRANT rds_iam TO {config['database']['iam_rwuser']};
        """)


    ## create the admin user role if not exists
    results = execute(connection, f"""
        SELECT 1 FROM pg_roles WHERE rolname='{config['database']['iam_admin']}'
    """)
    if not results:
        print('Creating IAM admin user:', config['database']['iam_admin'])
        results = execute(connection, f"""
            CREATE USER {config['database']['iam_admin']} WITH LOGIN;
            GRANT rds_iam TO {config['database']['iam_admin']};
        """)


    ## commit changes
    connection.commit()


## close the opened connection
finally:
    connection.close()



### IAM
iam = boto3.client('iam')


## get all policies
policies = []
pagination_token = None
while True:
    if pagination_token is None:
        response = iam.list_policies(
            Scope='Local'
        )
    else:
        response = iam.list_policies(
            Scope='Local',
            Marker=pagination_token
        )
    policies += response['Policies']
    pagination_token = response.get('Marker')
    if not pagination_token:
        break


## function to enable IAM user auth
def build_iam_for_rds(iam_user_name):
    policy_name = f"rds_auth-{config['project']['namespace']}-{args.stage}-{iam_user_name}"
    role_name = f"rds_auth-{config['project']['namespace']}-{args.stage}-{iam_user_name}"

    ## see if policy exists
    policy = None
    for _policy in policies:
        if _policy['PolicyName'] == policy_name:
            print('Policy found:', policy_name)
            policy = _policy


    ## if policy doesn't exist, create it
    # print('here', instance['DBInstanceArn'].split(':'))
    if policy is None:
        print('Creating Policy:', policy_name)
        resource_arn = ':'.join(['arn', 'aws', 'rds-db'] +
            instance['DBInstanceArn'].split(':')[3:5] +
            ['dbuser', instance['DbiResourceId']])
        # print(resource_arn)
        response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument = json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": [
                        "rds-db:connect"
                    ],
                    "Resource": [
                        f"{resource_arn}/{iam_user_name}"
                    ]
                }]
            }),
            Description='A policy to access RDS resources',
            # Tags=tags
        )
        policy = response['Policy']


    # ## check for role
    # try:
    #     response = iam.get_role(RoleName=role_name)
    #     role = response['Role']
    #     print('Role found:', role_name)
    #
    #
    # ## if it does not exist, create it
    # except iam.exceptions.NoSuchEntityException:
    #     print('Creating role:', role_name)
    #     response = iam.create_role(
    #         RoleName = role_name,
    #         AssumeRolePolicyDocument = json.dumps({
    #             "Version": "2012-10-17",
    #             "Statement": [{
    #                 "Effect": "Allow",
    #                 "Principal": {
    #                     "Service": ["lambda.amazonaws.com"]
    #                 },
    #                 "Action": [
    #                     "sts:AssumeRole"
    #                 ]
    #             }]
    #         }),
    #         Description = 'A role to access RDS resources',
    #         Tags = tags
    #     )
    #     role = response['Role']
    #
    #
    # ## Attach the Policy to the Role
    # print('Attaching Policy to Role')
    # response = iam.attach_role_policy(
    #     RoleName=role_name,
    #     PolicyArn=policy['Arn']
    # )


    ## update build_info
    return {
        'policy': policy,
        # 'role': role,
    }


## Build IAM Policy and Role for each IAM role:
build_info = {
    'iam_ruser':  build_iam_for_rds(config['database']['iam_ruser']),
    'iam_rwuser':  build_iam_for_rds(config['database']['iam_rwuser']),
    'iam_admin':  build_iam_for_rds(config['database']['iam_admin']),
}

def serialize(node):
    if isinstance(node, dict):
        return { key: serialize(value) for key, value in node.items() }
    if isinstance(node, list):
        return [serialize(value) for value in node]
    if isinstance(node, datetime):
        return node.strftime("%m/%d/%Y, %H:%M:%S")
    return node


## local dir
print('local_dir', local_dir)

with open(f'{local_dir}/../.build/{args.stage}.json', 'w') as f:
    json.dump(serialize(build_info), f)
