

def read_cookies(request):
    cookies = {}
    for cookie_str in request.headers.get('cookie', '').split(';'):
        try:
            name, value = cookie_str.strip().split('=')
        except ValueError:
            continue
        cookies[name] = value
    return cookies
