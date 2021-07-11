from chalice import Blueprint, BadRequestError, UnauthorizedError
import json
from ..orm.user import User
import hashlib
import os



blueprint = Blueprint(__name__)


@blueprint.route('/register', methods=['POST'], cors=True)
def POST_log_in():
    request = json.loads(blueprint.current_request.raw_body.decode())

    ## Check the contents of the request
    expected_args = ['first_name', 'last_name', 'email_address', 'username', 'password']
    if any(arg not in request for arg in expected_args):
        raise BadRequestError(
            f'missing all or some expected arguments from: {expected_args}'
        )

    ## Create the password salt and password hash
    password_salt = os.urandom(32) # Remember this
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
    print(new_user)

    ## Write new User record to DB

    return 'ok'


@blueprint.route('/login', methods=['POST'], cors=True)
def POST_log_in():
    request = json.loads(blueprint.current_request.raw_body.decode())

    ## Check the contents of the request
    expected_args = ['username', 'password']
    if any(arg not in request for arg in expected_args):
        return 400, f'missing all or some expected arguments from: {expected_args}'

    ## Load the matching User record from the DB

    ## Check the submitted password against the User password hash and salt
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        request['password'].encode('utf-8'), # Convert the password to bytes
        User.salt, # Provide the salt
        100000, # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128 # Get a 128 byte key
    )

    if password_hash == User.password_hash:
        ## Do login

        return 'ok'

    return UnauthorizedError('Bad password submitted')
