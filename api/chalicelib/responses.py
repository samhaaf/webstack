import chalice
from urllib.parse import quote_plus, unquote_plus


def generate_cookie_header(name, value, max_age=None, expires=None, path='/',
        domain=None, secure=False, http_only=True):
    """ <name>=<value>[; <Max-Age>=<age>]
        `[; expires=<date>][; domain=<domain_name>]
        [; path=<some_path>][; secure][; HttpOnly]"
    """

    header = f"{quote_plus(name)}={quote_plus(value)}"
    if max_age:
        header += f'; <Max-Age>={max_age}'
    if expires:
        ## TODO expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        raise NotImplementedError('`expires` header value not implemented')
    if path:
        header += f'; Path={path}'
    if domain:
        raise NotImplementedError('`domain` header value not implemented')
    if secure:
        raise NotImplementedError('`secure` header value not implemented')
    if http_only:
        header += '; HttpOnly'
    return header


def Response(status_code, body, headers={}):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": Response.blueprint.current_request.headers.get('origin', ''),
        'Access-Control-Allow-Credentials': 'true',
        'X-Custom-header': 'poop',
        **headers
    }
    print('Response.headers', headers)
    return chalice.Response(
        status_code = status_code,
        body = body,
        headers = headers
    )
