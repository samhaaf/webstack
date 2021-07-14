"""
    Takes the output from the . /generate.py script and applies it to an
        external .gen.json file

"""


from generate import generate_config, find_and_replace
from argparse import ArgumentParser
import hjson
import json
import os
from pprint import pprint

parser = ArgumentParser()
parser.add_argument('--input', '-i', type=str)
parser.add_argument('--pretty', '-p', action='store_true')
parser.add_argument('--stage', '-s', type=str)
args = parser.parse_args()

assert args.input, 'apply.py must run with an --input-file or -i argument'
assert args.stage, 'apply.py must be run with a --stage or -s argument'

def list_dir_recur(path):
    if not os.path.isdir(path):
        return [path]
    return sum([list_dir_recur(os.path.join(path, p)) for p in os.listdir(path)], [])

config = generate_config(stage=args.stage)

for file_path in list_dir_recur(args.input):
    *directory, file_name = file_path.split('/')
    file_split = file_name.split('.')
    if len(file_split) < 3 or file_split[-2] != 'gen':
        continue

    print(f'Applying config module to path={file_path}')

    with open(file_path) as f:
        target = hjson.load(f) if file_path[-5:] == '.json' else f.readlines()

    result = find_and_replace(config, target, lookup={'stage': args.stage})

    if file_path[-5:] == '.json':
        result = json.dumps(result, indent=4*args.pretty)
    else:
        result = ''.join(result)

    del file_split[-2]
    with open(os.path.join(*directory, '.'.join(file_split)), 'w') as f:
        f.write(result)
