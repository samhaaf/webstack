from chalice import Blueprint, BadRequestError, UnauthorizedError, AuthResponse, ConvertToMiddleware
import json
from ..orm.session import Session
from ..orm.objects import User, RefreshToken
from ..orm.io import dump
from ..tokens import encode_jwt, decode_jwt
import hashlib
import os
import time
from uuid import UUID
from pprint import pprint
from ..config import cors
from ..responses import Response
from ..requests import read_cookies


blueprint = Response.blueprint = Blueprint(__name__)


@blueprint.route('/register', methods=['POST'], cors=cors, content_types=['text/plain'])
def POST_register():
    request = json.loads(blueprint.current_request.raw_body.decode())


    ## Check the contents of the request
    expected_args = ['first_name', 'last_name', 'email_address', 'username', 'password']
    if any(arg not in request for arg in expected_args):
        raise BadRequestError(
            f'missing all or some expected arguments from: {expected_args}'
        )


    ## Start database session
    session = Session()
    try:

        ## Check if user already exists:
        match = session.query(User).filter(User.username == request['username']).first()
        if match:
            print(request)
            print(match)
            return Response(403, {
                "status": "failure",
                "message": "User already exists with given username"
            })

        match = session.query(User).filter(User.email_address == request['email_address']).first()
        if match:
            return Response(403, {
                "status": "failure",
                "message": "User already exists with given email address"
            })


        ## Create the password salt and password hash
        password_salt = os.urandom(32)  # Remember this
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            request['password'].encode('utf-8'), # Convert the password to bytes
            password_salt, # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128 # Get a 128 byte key
        )


        ## Create new User
        new_user = User(
            first_name = request['first_name'],
            last_name = request['last_name'],
            email_address = request['email_address'],
            username = request['username'],
            password_hash = password_hash,
            password_salt = password_salt,
        )
        session.add(new_user)
        session.commit()


        ## create new refresh token for this user
        new_refresh_token = RefreshToken(
            user_uid=new_user.uid,
            # ttl = 30,
        )
        session.add(new_refresh_token)
        session.commit()


        ## return
        return Response(200, {
                "status": "success",
                "refresh_token": dump(new_refresh_token),
                "user": dump(new_user, 'uid')
            }, set_cookie = {
                'name': 'refresh-token',
                'value': encode_jwt(dump(new_refresh_token)),
                'max_age': new_refresh_token.ttl
            }
        )

    ## Close database session
    finally:
        session.close()



@blueprint.route('/login', methods=['POST'], cors=cors, content_types=['text/plain'])
def POST_login():
    request = json.loads(blueprint.current_request.raw_body.decode())

    ## Check the contents of the request
    expected_args = ['username', 'password']
    if any(arg not in request for arg in expected_args):
        return 400, f'missing all or some expected arguments from: {expected_args}'


    # ## Open database session
    with Session() as session:

        ## Load the matching User record from the DB
        user = session.query(User).filter(User.username == request['username']).first()
        if user is None:
            return Response(403, {
                "status": "failure",
                "message": "No user found with the requested username"
            })


        ## Check the submitted password against the User password hash and salt
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            request['password'].encode('utf-8'), # Convert the password to bytes
            user.password_salt, # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256
            dklen=128 # Get a 128 byte key
        )


        ## If the password hashes don't match, fail
        if password_hash != user.password_hash:
            return Response(403, {
                'status': "failure",
                'message': 'incorrect password'
            })


        ## create new refresh token for this user
        new_refresh_token = RefreshToken(
            user_uid = user.uid,
            # ttl = 30,
        )
        session.add(new_refresh_token)
        session.commit()


        ## return
        return Response(200, {
                "status": "success",
                "refresh_token": dump(new_refresh_token),
                "user": dump(user, 'uid')
            }, set_cookie = {
                'name': 'refresh-token',
                'value': encode_jwt(dump(new_refresh_token)),
                'max_age': new_refresh_token.ttl
            }
        )



def check_refresh_token(session=None):

    ## Get refresh token from cookies
    refresh_token_cookie_string = read_cookies(blueprint.current_request).get('refresh-token')


    ## If no refresh-token cookie; refuse
    if not refresh_token_cookie_string:
        return Response(403, {
            'status': 'failure',
            'message': 'no refresh-token cookie',
            'refresh_token_invalidated': True
        }), None


    ## decrypt refresh_token
    try:
        refresh_token_cookie = decode_jwt(refresh_token_cookie_string)
    except:
        return Response(403, {
            'status': 'failure',
            'message': 'could not decode refresh-token',
            'refresh_token_invalidated': True
        }), None


    ## Assert that refresh token has valid format
    for ix, prop in enumerate(['uid', 'user_uid', 'ttl']):
        if prop not in refresh_token_cookie:
            print('invalid refresh_token_cookie:', refresh_token_cookie)
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token had invalid format [{ix}]',
                'refresh_token_invalidated': True
            }), None


    ## Open session
    _session = session or Session()
    try:

        print('refresh_token_cookie', refresh_token_cookie)
        print('uuid', UUID(refresh_token_cookie['uid']))
        ## Check that the RefreshToken exists
        refresh_token = _session.query(RefreshToken).filter(
            RefreshToken.uid == UUID(refresh_token_cookie['uid'])
        ).first()


        ## Determine if this is a valid UUID for the token
        if refresh_token is None:
            print('here')
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token has does not exist in database',
                'refresh_token_invalidated': True
            }), None


        ## Determine if refresh token has expired
        if refresh_token.expired:
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token has expired',
                'refresh_token_invalidated': True
            }), None


        ## Determine if refresh token has been invalidated
        if refresh_token.invalidated:
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token has been invalidated',
                'refresh_token_invalidated': True
            }), None


        return None, {
            **refresh_token_cookie,
            'time_left': refresh_token.time_left
        }

    ## Close database session, if applicable
    finally:
        if session is None:
            _session.close()



@blueprint.route('/refresh_token', methods=['GET'], cors=cors)
def GET_refresh_token():

    ## Open database session
    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error


        ## create new refresh token for this user
        new_refresh_token = RefreshToken(
            user_uid = refresh_token['user_uid'],
            # ttl = 30,
        )
        session.add(new_refresh_token)
        session.commit()


        ## return
        return Response(200, {
                "status": "success",
                "refresh_token": dump(new_refresh_token)
            }, set_cookie = {
                'name': 'refresh-token',
                'value': encode_jwt(dump(new_refresh_token)),
                'max_age': new_refresh_token.time_left
            }
        )



@blueprint.route('/refresh_token/check', methods=['GET'], cors=cors)
def GET_refresh_token_check():

    ## Check the refresh token
    error, refresh_token = check_refresh_token()
    if error:
        return error


    ## return
    return Response(200, {
        "status": "success",
        "refresh_token": refresh_token
    })



@blueprint.route('/refresh_token/invalidate', methods=['GET'], cors=cors)
def GET_refresh_token_invalidate():

    ## Open database session
    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error


        ## invalidate the token
        refresh_token_record = session.query(RefreshToken).filter(
            RefreshToken.uid == UUID(refresh_token['uid'])
        ).first()
        refresh_token_record.invalidated = True


         ## add and commit
        session.add(refresh_token_record)
        session.commit()


        ## return
        return Response(200, {
            "status": "success",
            "refresh_token": dump(refresh_token_record)
        })



@blueprint.route('/access_token', methods=['GET'], cors=cors)
def GET_access_token():

    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error

        ## Assert user has not been banned
        user = session.query(User).filter(User.uid == UUID(refresh_token['user_uid'])).first()
        if user.banned:
            Response(
                status_code = 403,
                body = {
                    "status": "failure",
                    "message": "User has been banned"
                },
                headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": blueprint.current_request.headers.get('origin', '*'),
                    'Access-Control-Allow-Credentials': 'true',
                }
            )


    ## create new refresh token for this user
    access_token = {
        'class': 'base',
        'ttl': 600,
        'refresh_token_uid': str(refresh_token['uid']),
        'user_uid': str(refresh_token['user_uid']),
        'created_at': time.time()
    }


    ## return
    return Response(
        status_code = 200,
        body = {
            "status": "success",
            "access_token": access_token
        }, set_cookie = {
            'name': 'access-token',
            'value': encode_jwt(access_token),
            'max_age': access_token['ttl']
        }
    )



def check_access_token():

    ## Get access token from cookies
    access_token_cookie_string = read_cookies(blueprint.current_request).get('access-token')


    ## If no access token cookie; refuse
    if not access_token_cookie_string:
        return Response(403, {
            'status': 'failure',
            'message': 'no access-token cookie',
            'access_token_invalidated': True
        }), None


    ## decrypt access token
    try:
        access_token = decode_jwt(access_token_cookie_string)
    except:
        return Response(403, {
            'status': 'failure',
            'message': 'could not decode access-token',
            'access_token_invalidated': True
        }), None


    ## Assert that access token has valid format
    for ix, prop in enumerate(['class', 'user_uid', 'refresh_token_uid', 'ttl', 'created_at']):
        if prop not in access_token:
            return Response(403, {
                'status': 'failure',
                'message': f'access token had invalid format [{ix}]',
                'access_token_invalidated': True
            }), None


    ## Assert that the access token has not expired
    if time.time() - access_token['created_at'] > access_token['ttl']:
        return Response(403, {
            'status': 'failure',
            'message': 'access-token expired',
            'access_token_invalidated': True
        }), None

    access_token['time_left'] = access_token['ttl'] - time.time() + access_token['created_at']

    return None, access_token



@blueprint.route('/access_token/check', methods=['GET'], cors=cors)
def GET_access_token_check():

    ## Check the refresh token
    error, access_token = check_access_token()
    if error:
        return error

    ## return
    return Response(200, {
        "status": "success",
        'access_token': access_token
    })
