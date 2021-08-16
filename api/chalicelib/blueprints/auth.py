from chalice import Blueprint, BadRequestError, UnauthorizedError, AuthResponse, ConvertToMiddleware
import json
from ..orm import Session
from ..orm.users import User
from ..orm.tokens import RefreshToken
from ..tokens import encode_jwt, decode_jwt, create_refresh_token, is_refresh_token_valid
import hashlib
import os
import time
from pprint import pprint
from ..config import cors
from ..responses import Response, generate_cookie_header
# from ..middleware import register_middleware,


blueprint = Response.blueprint = Blueprint(__name__)
# register_middleware(blueprint, format_response)



@blueprint.route('/register', methods=['POST'], cors=cors)
# @format_response
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


        ## Write new User record to DB
        session.add(new_user)
        session.commit()


        return Response(200, {
            "status": "success"
        })

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
        new_refresh_token = create_refresh_token(
            user.sid,
            # ttl = 30,
            session=session
        )


        ## return
        return Response(200, {
                "status": "success",
                "ttl": new_refresh_token.time_left,
                "refresh_token_sid": new_refresh_token.sid
            },
            headers = {
                "Set-Cookie": generate_cookie_header(
                    name = 'refresh-token',
                    value = encode_jwt({
                        "sid": new_refresh_token.sid,
                        "ttl": new_refresh_token.time_to_live,
                        "user_sid": new_refresh_token.user_sid
                    }),
                    http_only = True,
                    max_age = new_refresh_token.time_left
            )}
        )



def check_refresh_token(session=None):

    ## Get refresh token from cookies
    refresh_token_cookie_string = None
    for cookie_str in blueprint.current_request.headers.get('cookie', '').split(';'):
        print('cookie_str', repr(cookie_str))
        try:
            name, value = cookie_str.strip().split('=')
        except ValueError:
            continue
        if name == 'refresh-token':
            refresh_token_cookie_string = value


    ## If no refresh-token cookie; refuse
    if not refresh_token_cookie_string:
        print(1)
        return Response(403, {
            'status': 'failure',
            'message': 'no refresh-token cookie'
        }), None


    ## decrypt refresh_token
    try:
        refresh_token_cookie = decode_jwt(refresh_token_cookie_string)
    except:
        print(2)
        return Response(403, {
            'status': 'failure',
            'message': 'could not decode refresh-token'
        }), None


    ## Assert that refresh token has valid format
    for ix, prop in enumerate(['sid', 'user_sid', 'ttl']):
        if prop not in refresh_token_cookie:
            print(3)
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token had invalid format [{ix}]'
            }), None


    ## Open session
    _session = session or Session()
    try:

        ## Check that the RefreshToken exists
        refresh_token = _session.query(RefreshToken).filter(
            RefreshToken.sid == refresh_token_cookie['sid']
        ).first()


        ## Determine if refresh token has expired
        if refresh_token.expired:
            print(4)
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token has expired'
            }), None


        ## Determine if refresh token has been invalidated
        if refresh_token.invalidated:
            print('refresh token sid', refresh_token.sid)
            print(5)
            return Response(403, {
                'status': 'failure',
                'message': f'refresh token has been invalidated'
            }), None


        return None, refresh_token_cookie

    ## Close database session, if applicable
    finally:
        if session is None:
            _session.close()



@blueprint.route('/new_refresh_token', methods=['GET'], cors=cors)
def new_refresh_token():

    ## Open database session
    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error


        ## create new refresh token for this user
        new_refresh_token = create_refresh_token(
            refresh_token['user_sid'],
            # ttl = 30,
            session = session
        )


        ## return
        return Response(200, {
                "status": "success",
                "ttl": new_refresh_token.time_left,
                "refresh_token_sid": new_refresh_token.sid
            },
            headers = {
                "Set-Cookie": generate_cookie_header(
                    name = 'refresh-token',
                    value = encode_jwt({
                        "sid": new_refresh_token.sid,
                        "ttl": new_refresh_token.time_to_live,
                        "user_sid": new_refresh_token.user_sid
                    }),
                    http_only = True,
                    max_age = new_refresh_token.time_left
            )}
        )



@blueprint.route('/check_refresh_token', methods=['GET'], cors=cors)
def _check_refresh_token():

    ## Check the refresh token
    error, refresh_token = check_refresh_token()
    if error:
        print('/check_refresh_token error')
        return error

    print('Got refresh token', refresh_token)

    ## return
    return Response(200, {
        "status": "success",
        "refresh_token_sid": refresh_token['sid']
    })



@blueprint.route('/invalidate_refresh_token', methods=['GET'], cors=cors)
def invalidate_refresh_token():

    ## Open database session
    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error


        ## invalidate the token
        token_record = session.query(RefreshToken).filter(
            RefreshToken.sid == refresh_token['sid']
        ).first()
        token_record.invalidated = True

         ## add and commit
        session.add(token_record)
        session.commit()


        ## return
        return Response(200, {
            "status": "success",
            "refresh_token_sid": refresh_token['sid']
        })



@blueprint.route('/new_access_token', methods=['GET'], cors=cors)
def new_access_token():

    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error

        # ## Assert user has not been banned
        # user = session.query(User).filter(User.sid == refresh_token['user_sid']).first()
        # if user.banned:
        #     Response(
        #         status_code = 403,
        #         body = {
        #             "status": "failure",
        #             "message": "User has been banned"
        #         },
        #         headers = {
        #             "Content-Type": "application/json",
        #             "Access-Control-Allow-Origin": blueprint.current_request.headers.get('origin', '*'),
        #             'Access-Control-Allow-Credentials': 'true',
        #         }
        #     )


    ## create new refresh token for this user
    access_token = {
        'class': 'base',
        'ttl': 600,
        'refresh_token_sid': refresh_token['sid'],
        'user_sid': refresh_token['user_sid'],
        'created_at': time.time()
    }


    ## return
    return Response(
        status_code = 200,
        body = {
            "status": "success",
            "ttl": access_token['ttl'],
            "refresh_token_sid": refresh_token['sid'],
        },
        headers = {
            "Set-Cookie": generate_cookie_header(
                name = 'access-token',
                value = encode_jwt(access_token),
                http_only = True,
                max_age = access_token['ttl']
        )}
    )



def check_access_token():

    ## Get access token from cookies
    access_token_cookie_string = None
    for cookie_str in blueprint.current_request.headers.get('cookie', '').split(';'):
        name, value = cookie_str.strip().split('=')
        if name == 'access-token':
            access_token_cookie_string = value


    ## If no access token cookie; refuse
    if not access_token_cookie_string:
        return Response(403, {
            'status': 'failure',
            'message': 'no access-token cookie'
        }), None


    ## decrypt access token
    try:
        access_token = decode_jwt(access_token_cookie_string)
    except:
        return Response(403, {
            'status': 'failure',
            'message': 'could not decode access-token'
        }), None


    ## Assert that access token has valid format
    for ix, prop in enumerate(['class', 'user_sid', 'refresh_token_sid', 'ttl', 'created_at']):
        if prop not in access_token:
            return Response(403, {
                'status': 'failure',
                'message': f'access token had invalid format [{ix}]'
            }), None


    ## Assert that the access token has not expired
    if time.time() - access_token['created_at'] > access_token['ttl']:
        return Response(403, {
            'status': 'failure',
            'message': 'access-token expired'
        }), None

    return None, access_token



@blueprint.route('/check_access_token', methods=['GET'], cors=cors)
def _check_access_token():

    ## Check the refresh token
    error, access_token = check_access_token()
    if error:
        return error

    ## return
    return Response(200, {
        "status": "success",
        "access_token_sid": access_token['sid']
    })
