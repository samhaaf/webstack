import chalice
from urllib.parse import quote_plus, unquote_plus
from .config import is_https


def generate_cookie_header(name, value, max_age=None, expires=None, path='/',
        domain=None, secure=False, http_only=True, same_site=None):
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
        header += f'; Domain={domain}'
    if secure:
        header += '; Secure'
        # raise NotImplementedError('`secure` header value not implemented')
    if http_only:
        header += '; HttpOnly'
    if same_site:
        header += '; SameSite=' + same_site
    return header


def Response(status_code, body, headers={}, set_cookie={}):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": Response.blueprint.current_request.headers.get('origin', ''),
        'Access-Control-Allow-Credentials': 'true',
        'X-Custom-header': 'poop',
        **headers
    }
    # print('Request headers', (Response.blueprint.current_request.headers))
    # print('Response.headers', headers)
    if set_cookie:
        headers["Set-Cookie"] = generate_cookie_header(
            name = set_cookie['name'],
            value = set_cookie['value'],
            http_only = set_cookie.get('http_only', True),
            secure = set_cookie.get('secure', is_https),
            same_site = set_cookie.get('same_site', 'None' if is_https else None),
            path = set_cookie.get('path', '/'),
            domain = set_cookie.get('domain'),
            max_age = set_cookie.get('max_age'),
            # domain = Response.blueprint.current_request['host'],
        )
    return chalice.Response(
        status_code = status_code,
        body = body,
        headers = headers
    )
