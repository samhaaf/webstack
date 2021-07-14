
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
if process.stdout.decode()[:4] == 'make':
    config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')[1:-1]))
else:
    config = json.loads('\n'.join(process.stdout.decode().strip().split('\n')))


## Init docker image
process = subprocess.run(
    [   'sudo', 'docker', 'rm',
        f"{config['project']['name']}-postgres-{args.stage}"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
if process.stderr:
    raise RuntimeError(
        f'Error starting docker in start_image.py:\n\n{process.stderr.decode()}'
    )
