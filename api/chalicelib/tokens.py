import jwt
import json
import time
from datetime import datetime
from .orm import Session
from .orm.users import User
from .orm.tokens import RefreshToken
from .config import config
import uuid


def encode_jwt(payload):
    return jwt.encode(payload, config['jwt_secret'], algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, config['jwt_secret'], algorithms=["HS256"])


def create_refresh_token(user_uid, ttl=7*24*60*60, session=None):  # default 1-week

    if isinstance(user_uid, str):
        user_uid = uuid.UUID(user_uid)

    expunge_all = False
    if session is None:
        session = Session()
        expunge_all = True

    token = RefreshToken(
        created_at = datetime.now(),
        user_uid = user_uid,
        time_to_live = ttl
    )

    session.add(token)
    session.commit()

    if expunge_all:
        session.expunge_all()
        session.close()

    return token


def invalidate_refresh_token(token_uid):
    with Session() as session:

        if isinstance(token_uid, str):
            token_uid = uuid.UUID(token_uid)

        token = session.query(RefreshToken).filter(RefreshToken.uid == token_uid).first()

        if token is None:
            return False

        token.invalidated = True

        session.add(token)
        session.commit()

    return True



def is_refresh_token_valid(token_uid):
    session = Session()

    token = session.query(RefreshToken).filter(RefreshToken.uid == token_uid).first()

    if token is None:
        return False

    if time.time() - token.created_at.timestamp() > token.time_to_live:
        return False

    if token.invalidated:
        return False

    return True
