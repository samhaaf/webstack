import jwt
import json
import time
from datetime import datetime
from .config import config
import uuid
import random


def encode_jwt(payload):
    payload['noise']: random.random()
    return jwt.encode(payload, config['jwt_secret'], algorithm="HS256")


def decode_jwt(token):
    payload = jwt.decode(token, config['jwt_secret'], algorithms=["HS256"])
    if payload.get('noise'):
        del payload['noise']
    return payload
