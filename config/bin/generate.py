"""
    Loads the .gen.hjson files using hjson, applies search-and-replace, and
        returns one single aggregate json blob

: command line args
    --config-dir:       where to load the config files from

"""


import os
import re
import hjson
import json
from pprint import pprint
import argparse
import copy

local_dir = os.path.dirname(os.path.realpath(__file__))


def assimilate(dict_1, dict_2, *keychain):
    assert isinstance(dict_1, dict), "assimilate only works on dict types"
    assert isinstance(dict_2, dict), "assimilate only works on dict types"
    for key, value in dict_2.items():
        keychain = keychain + (key,)
        if key not in dict_1:
            dict_1[key] = value
        else:
            long_key = '.'.join(keychain)
            if not isinstance(dict_1[key], dict):
                raise ValueError(
                    f'Attempting to overwrite key {long_key}'
                )
            if not isinstance(value, dict):
                raise ValueError(
                    f'Attemption to merge non-dict with dict at key: {long_key}'
                )
            assimilate(dict_1[key], value, *keychain)
    return dict_1


def multikey_index(value, keychain, _idx=0, graceful=False):
    if _idx == len(keychain):
        return value

    try:
        if isinstance(value, dict):
            subset = value[keychain[_idx]]
        elif isinstance(value, list):
            try:
                subset = value[int(keychain[_idx])]
            except ValueError:
                raise ValueError(f'Expected int key at keychain: {keychain[:_idx+1]}')
        else:
            raise ValueError(
                f'Non-indexible type for given keychain: {keychain[:_idx+1]}'
            )
    except (IndexError, KeyError, ValueError) as e:
        if graceful:
            return None
        print(f'error indexing value for given keychain: {keychain[:_idx+1]}')
        raise

    return multikey_index(subset, keychain, _idx=_idx+1, graceful=graceful)


def find_and_replace(config, target, lookup={}, graceful=False):

    ## TODO: if a reference references another reference, defer

    if isinstance(target, dict):
        # this no longer works because we need access to new neighbor values:
        # return {key: recur(val) for key,val in target.items()}
        for key in target.keys():
            target[key] = find_and_replace(config, target[key], lookup=lookup, graceful=graceful)

    if isinstance(target, list):
        return [find_and_replace(config, val, lookup=lookup, graceful=graceful) for val in target]

    if isinstance(target, str):

        ## replace controls matching #{} syntax with that value found in lookup
        while True:
            replace_matches = re.finditer('\#\{[A-Za-z0-9._]*\}', target)
            try:
                match = next(replace_matches)
            except StopIteration:
                break
            keychain = match.group()[2:-1].split('.')
            span = match.span()
            new_value = multikey_index(lookup, keychain, graceful=graceful or not lookup)
            if new_value is not None:
                target = target[:span[0]] + new_value + target[span[1]:]
            else:
                raise NotImplementedError(
                    'Unhandled case where #{} lookup returns None'
                )


        ## replace controls matching %{} syntax with file content found at path
        if re.match('^\%\{[A-Za-z0-9._/]*\}$', target):
            path = target[2:-1]
            try:
                with open(path, 'r') as f:
                    if path.split('.')[-1] in ['json', 'hjson']:
                        return json.load(f)
                    else:
                        return f.read()
            except FileNotFoundError:
                return None

        ## replace controls matching ${} syntax with that value found in config
        while True:
            replace_matches = re.finditer('\$\{[A-Za-z0-9._]*\}', target)
            try:
                match = next(replace_matches)
            except StopIteration:
                break
            keychain = match.group()[2:-1].split('.')
            span = match.span()
            new_value = multikey_index(config, keychain, graceful=graceful)
            ## If the new value is not a string, we might replace the whole thing
            if not isinstance(new_value, str):
                ## If the span stretches the whole target, we assume a total replace
                if span[0] == 0 and span[1] == len(target):
                    target = new_value
                    break
                new_value = str(new_value)
            target = target[:span[0]] + new_value + target[span[1]:]

    return target


def generate_config(stage=None, graceful=True):
    with open(f'{local_dir}/../public.gen.hjson') as f:
        config = hjson.load(f)

    with open(f'{local_dir}/../private.gen.hjson') as f:
        new_info = hjson.load(f)
        assimilate(config, new_info)

    config = find_and_replace(config, config, graceful=graceful)

    if stage is not None:
        assert stage in config['stages'], f'unexpected stage: `{stage}`'
        subset = copy.deepcopy(config)
        del subset['stages']
        return assimilate(subset, config['stages'][stage])

    return config



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', '-s', type=str)
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()

    print(json.dumps(generate_config(args.stage, graceful=not args.debug), indent=4))
