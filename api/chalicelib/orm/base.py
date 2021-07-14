from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from urllib.parse import quote_plus

Base = declarative_base()

with open('./vendor/config.json') as f:
    config = json.load(f)

db = config['database']

if db['type'] == 'postgres':
    engine = create_engine(
        f'postgresql+psycopg2://{db["username"]}:{quote_plus(db["password"])}@{db["host"]}:{db["port"]}/{db["name"]}'
    )
else:
    raise RuntimeError('Unhandled database type:', db['type'])


# create a configured "Session" class
Session = sessionmaker(bind=engine)
