from chalice import Blueprint, BadRequestError, UnauthorizedError, AuthResponse, Response
import json
from ..orm import Session
from ..orm.users import User
from ..orm.tokens import RefreshToken
from ..tokens import encode_jwt, decode_jwt, create_refresh_token, is_refresh_token_valid
from ..cookies import generate_cookie_header
import hashlib
import os
import time
from pprint import pprint


blueprint = Blueprint(__name__)



@blueprint.route('/register', methods=['POST'], cors=True)
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
            return {
                "status": "failure",
                "message": "User already exists with given username"
            }

        match = session.query(User).filter(User.email_address == request['email_address']).first()
        if match:
            return {
                "status": "failure",
                "message": "User already exists with given email address"
            }


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


        return {
            "status": "success"
        }

    ## Close database session
    finally:
        session.close()



@blueprint.route('/login', methods=['POST'], cors=True, content_types=['text/plain'])
def POST_login():
    request = json.loads(blueprint.current_request.raw_body.decode())


    ## Check the contents of the request
    expected_args = ['username', 'password']
    if any(arg not in request for arg in expected_args):
        return 400, f'missing all or some expected arguments from: {expected_args}'


    ## Open database session
    with Session() as session:

        ## Load the matching User record from the DB
        user = session.query(User).filter(User.username == request['username']).first()
        if user is None:
            return {
                "status": "failure",
                "message": "No user found with the requested username"
            }


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
            return {
                'status': "failure",
                'message': 'incorrect password'
            }


        ## create new refresh token for this user
        new_refresh_token = create_refresh_token(user.sid, session=session)
        print('refresh token sid', new_refresh_token.sid)

        headers = {
            "Content-Type": "application/json",
            "Set-Cookie": generate_cookie_header(
                name = 'refresh-token',
                value = encode_jwt({
                    "sid": new_refresh_token.sid,
                    "ttl": new_refresh_token.time_to_live,
                    "user_sid": new_refresh_token.user_sid
                }),
                http_only = True,
                max_age = new_refresh_token.time_left
            ),
            "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
            'Access-Control-Allow-Credentials': 'true',
        }

        ## return
        return Response(
            status_code = 200,
            body = {
                "status": "success",
                "time_left": new_refresh_token.time_left,
                "refresh_token_sid": new_refresh_token.sid
            },
            headers = headers
        )




def check_refresh_token(session=None):

    ## Get refresh token from cookies
    refresh_token_cookie_string = None
    for cookie_str in blueprint.current_request.headers.get('cookie', '').split(';'):
        name, value = cookie_str.strip().split('=')
        if name == 'refresh-token':
            refresh_token_cookie_string = value


    ## If no refresh-token cookie; refuse
    if not refresh_token_cookie_string:
        return Response(
            status_code = 403,
            body = {
                'status': 'failure',
                'message': 'no refresh-token cookie'
            },
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        ), None


    ## decrypt refresh_token
    try:
        refresh_token_cookie = decode_jwt(refresh_token_cookie_string)
    except:
        return Response(
            status_code = 403,
            body = {
                'status': 'failure',
                'message': 'could not decode refresh-token'
            },
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        ), None


    ## Assert that refresh token has valid format
    for ix, prop in enumerate(['sid', 'user_sid', 'ttl']):
        if prop not in refresh_token_cookie:
            return Response(
                status_code = 403,
                body = {
                    'status': 'failure',
                    'message': f'refresh token had invalid format [{ix}]'
                },
                headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                    'Access-Control-Allow-Credentials': 'true',
                }
            ), None


    ## Open session
    _session = session or Session()
    try:

        ## Check that the RefreshToken exists
        refresh_token = _session.query(RefreshToken).filter(
            RefreshToken.sid == refresh_token_cookie['sid']
        ).first()


        ## Determine if refresh token has expired
        if refresh_token.expired:
            return Response(
                status_code = 403,
                body = {
                    'status': 'failure',
                    'message': f'refresh token has expired'
                },
                headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                    'Access-Control-Allow-Credentials': 'true',
                }
            ), None


        ## Determine if refresh token has been invalidated
        if refresh_token.invalidated:
            print('refresh token sid', refresh_token.sid)
            return Response(
                status_code = 403,
                body = {
                    'status': 'failure',
                    'message': f'refresh token has been invalidated'
                },
                headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                    'Access-Control-Allow-Credentials': 'true',
                }
            ), None


        return None, refresh_token_cookie

    ## Close database session, if applicable
    finally:
        if session is None:
            _session.close()



@blueprint.route('/new_refresh_token', methods=['GET'], cors=True)
def new_refresh_token():

    ## Open database session
    with Session() as session:

        ## Check the refresh token
        error, refresh_token = check_refresh_token(session=session)
        if error:
            return error


        ## create new refresh token for this user
        new_refresh_token = create_refresh_token(refresh_token['user_sid'], session=session)


        ## return
        return Response(
            status_code = 200,
            body = {
                "status": "success",
                "time_left": new_refresh_token.time_left,
                "refresh_token_sid": new_refresh_token.sid
            },
            headers = {
                "Content-Type": "application/json",
                "Set-Cookie": generate_cookie_header(
                    name = 'refresh-token',
                    value = encode_jwt({
                        "sid": new_refresh_token.sid,
                        "ttl": new_refresh_token.time_to_live,
                        "user_sid": new_refresh_token.user_sid
                    }),
                    http_only = True,
                    max_age = new_refresh_token.time_left
                ),
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        )



@blueprint.route('/check_refresh_token', methods=['GET'], cors=True)
def _check_refresh_token():

    ## Check the refresh token
    error, refresh_token = check_refresh_token()
    if error:
        return error

    ## return
    return Response(
        status_code = 200,
        body = {
            "status": "success",
            "refresh_token_sid": refresh_token['sid']
        },
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
            'Access-Control-Allow-Credentials': 'true',
        }
    )



@blueprint.route('/invalidate_refresh_token', methods=['GET'], cors=True)
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
        return Response(
            status_code = 200,
            body = {
                "status": "success",
                "refresh_token_sid": refresh_token['sid']
            },
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        )



@blueprint.route('/new_access_token', methods=['GET'], cors=True)
def new_access_token():

    ## Check the refresh token
    error, refresh_token = check_refresh_token()
    if error:
        return error


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
            "access_token_sid": access_token['sid']
        },
        headers = {
            "Content-Type": "application/json",
            "Set-Cookie": generate_cookie_header(
                name = 'access-token',
                value = encode_jwt(access_token),
                http_only = True,
                max_age = access_token['ttl']
            ),
            "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
            'Access-Control-Allow-Credentials': 'true',
        }
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
        return Response(
            status_code = 403,
            body = {
                'status': 'failure',
                'message': 'no access-token cookie'
            },
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        ), None


    ## decrypt access token
    try:
        access_token = decode_jwt(access_token_cookie_string)
    except:
        return Response(
            status_code = 403,
            body = {
                'status': 'failure',
                'message': 'could not decode access-token'
            },
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        ), None


    ## Assert that access token has valid format
    for ix, prop in enumerate(['class', 'user_sid', 'refresh_token_sid', 'ttl', 'created_at']):
        if prop not in access_token:
            return Response(
                status_code = 403,
                body = {
                    'status': 'failure',
                    'message': f'access token had invalid format [{ix}]'
                },
                headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                    'Access-Control-Allow-Credentials': 'true',
                }
            ), None


    ## Assert that the access token has not expired
    if time.time() - access_token['created_at'] > access_token['ttl']:
        return Response(
            status_code = 403,
            body = {
                'status': 'failure',
                'message': 'access-token expired'
            },
            headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
                'Access-Control-Allow-Credentials': 'true',
            }
        ), None

    return None, access_token



@blueprint.route('/check_access_token', methods=['GET'], cors=True)
def _check_access_token():

    ## Check the refresh token
    error, access_token = check_access_token()
    if error:
        return error

    ## return
    return Response(
        status_code = 200,
        body = {
            "status": "success",
            "access_token_sid": access_token['sid']
        },
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": blueprint.current_request.headers['origin'],
            'Access-Control-Allow-Credentials': 'true',
        }
    )
