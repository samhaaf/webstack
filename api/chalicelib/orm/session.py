from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from urllib.parse import quote_plus
import boto3
from ..config import config


def Session():
    db = config['database']

    if db['build'] == 'docker':
        engine = create_engine(
            f'postgresql+psycopg2://{db["username"]}:{quote_plus(db["password"])}@{db["host"]}:{db["port"]}/{db["name"]}'
        )
    elif db['build'] == 'rds':
        ## get instance
        rds = boto3.client('rds')
        response = rds.describe_db_instances(DBInstanceIdentifier=db['identifier'])
        instance = response['DBInstances'][0]

        ## generate auth token
        auth_token = rds.generate_db_auth_token(
            DBHostname = instance['Endpoint']['Address'],
            Port = instance['Endpoint']['Port'],
            DBUsername = config['database']['iam_rwuser'],
        )

        ## build engine
        engine = create_engine(
            f'postgresql+psycopg2://{db["iam_rwuser"]}:{quote_plus(auth_token)}@{instance["Endpoint"]["Address"]}:{instance["Endpoint"]["Port"]}/{db["name"]}'
        )
    else:
        raise RuntimeError('Unhandled database build:', db['build'])

    # create a configured "Session" class
    return sessionmaker(bind=engine)()
