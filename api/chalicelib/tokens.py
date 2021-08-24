import jwt
import json
import time
from datetime import datetime
from .config import config
import uuid


def encode_jwt(payload):
    return jwt.encode(payload, config['jwt_secret'], algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, config['jwt_secret'], algorithms=["HS256"])
