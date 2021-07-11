
import argparse
import os, subprocess
import json
from pprint import pprint


## Parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('--stage', '-s', type=str, default=None)
args = parser.parse_args()


## assert stage argument is set
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


## Init docker image
process = subprocess.run(
    [   'sudo', 'docker', 'create',
        '--name', f"{config['project']['name']}-postgres-{args.stage}",
        '--env', f"POSTGRES_DB={config['database']['name']}",
        '--env', f"POSTGRES_USER={config['database']['username']}",
        '--env', f"POSTGRES_PASSWORD={config['database']['password']}",
        '-p', f'{config["database"]["host"]}:{config["database"]["port"]}:5432/tcp',
        'postgres'
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
if process.stderr:
    raise RuntimeError(
        f'Error starting docker in start_image.py:\n\n{process.stderr.decode()}'
    )
