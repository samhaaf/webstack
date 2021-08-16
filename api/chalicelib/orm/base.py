from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from urllib.parse import quote_plus
import boto3
from ..config import config

Base = declarative_base()

db = config['database']

if db['build'] == 'docker':
    engine = create_engine(
        f'postgresql+psycopg2://{db["username"]}:{quote_plus(db["password"])}@{db["host"]}:{db["port"]}/{db["name"]}'
    )

elif db['build'] == 'rds':

    rds = boto3.client('rds')

    ## get instance
    response = rds.describe_db_instances(DBInstanceIdentifier=config['database']['identifier'])
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
Session = sessionmaker(bind=engine)
