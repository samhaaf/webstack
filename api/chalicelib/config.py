import json
import os


with open(f'./chalicelib/vendor/config.json') as f:
    config = json.load(f)


cors = config['api'].get('cors')

is_https = config['api'].get('is_https')
