
import argparse
import os, subprocess
import json
from pprint import pprint
from sql_utils import psycopg2, execute, execute_insert_from_dict_list
from collections import OrderedDict


## Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('--stage', '-s', type=str, default=None)
args = parser.parse_args()


## assert stage argument is set
assert args.stage is not None, '--stage argument expected'


## get local directory
local_dir = os.path.dirname(os.path.realpath(__file__))


## get config
os.chdir(f"{local_dir}/../../config/")
process = subprocess.run(
    ['make','print', f'stage={args.stage}'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
if process.stderr:
    raise RuntimeError(f'In config/bin/generate.py:\n\n{process.stderr.decode()}')
if process.stdout.decode()[:4] == 'make':
    config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')[1:-1]))
else:
    config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')))


## connect
connection = psycopg2.connect(
    host = config['database']['host'],
    port = config['database']['port'],
    dbname = config['database']['name'],
    user = config['database']['username'],
    password = config['database']['password']
)


## get list of all tables in the schema
records = execute(connection, """
    SELECT table_schema, table_name FROM information_schema.tables
    WHERE table_schema = 'public'
""")


## if the _update_event table does not exist: create it
if '_update_event' not in [record['table_name'] for record in records]:
    print('Creating `_update_event` table in database and initiating version 0')
    execute(connection, """
        CREATE TABLE public."_update_event"
        (
            sid serial NOT NULL,
            created_at timestamp not null default now(),
            updated_at timestamp not null default now(),
            deleted_at timestamp null,
            name varchar null,
            CONSTRAINT _update_event_sid_pk PRIMARY KEY (sid)
        );

        ALTER TABLE public."_update_event"
            OWNER to postgres;
    """)
    connection.commit()


## determine which version the database is on
records = execute(connection, """
    SELECT name FROM _update_event
    ORDER BY updated_at DESC
    LIMIT 1
""")
last_update = records[0]['name'] if records else ''


## build list of updates to do
all_updates = os.listdir(f"{local_dir}/../updates/")
do_updates = []
for update in all_updates:
    if update <= last_update:
        continue
    if len(update.split('.')) == 3 and args.stage not in update.split('.')[1].split(','):
        continue
    do_updates.append(update)


## print if there are no updates to do
if not do_updates:
    print('No updates to perform')


## for each update: run, record
for filename in do_updates:

    ## Do update
    print('Doing update:', filename)
    dtype = filename.split('.')[-1]

    ## SQL-type update
    if dtype == 'psql' or dtype == 'sql':
        with open(f'{local_dir}/../updates/{filename}') as f:
            execute(connection, '\n'.join(f.readlines()))

    ## Data-insert style update (JSON)
    elif dtype == 'json':
        with open(f'{local_dir}/../updates/{filename}') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
        for table_name, rows in data.items():
            execute_insert_from_dict_list(connection, table_name, rows)

    else:
        raise RuntimeError('Unexpected data type:', dtype)

    ## record update event
    execute(connection, f"""
        INSERT INTO _update_event (name) VALUES ('{filename}')
    """)
    connection.commit()
