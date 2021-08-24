import json
from chalice import Blueprint
from ..config import cors
from ..responses import Response


blueprint = Response.blueprint = Blueprint(__name__)

OBJECTS = {}


@blueprint.route('/test', methods=['GET'], cors=cors)
def GET_test():
    return {'key': 'value'}


@blueprint.route('/objects/{key}', methods=['GET', 'PUT'], cors=cors)
def GET_myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)


@blueprint.route('/products', methods=['GET'], cors=cors)
def GET_products():
    scope = ['https://spreadsheets.google.com/feeds']
    SPREADSHEET_KEY = '1c919wtwvSx_tbBcIVXO4DLF5nwxsjH7pHTIfQa8u3Ao'
    RANGE = 'Inventory!A1:E'

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        '../vendor/credentials.json',
        scope
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_KEY)
    print(sheet)
    worksheet = ws = sheet.worksheet('Products')
    cell = ws.acell('B1:E')
    row = ws.row_values(1)

    records = worksheet.get_all_records()
    formatted = [
        {key.replace(' ', '_').lower(): value for key,value in record.items()}
        for record in records
    ]

    return formatted


@blueprint.route('/set_cookie', methods=['POST'], cors=cors, content_types=['text/plain'])
def POST_dev_set_cookie():
    request = json.loads(blueprint.current_request.raw_body.decode())

    print('Setting cookie', dict(
        name = 'simple_key',
        value = 'simple_value',
        http_only = request.get('http_only', False),
        domain = request.get('domain'),
        same_site = request.get('same_site'),
        path = request.get('path', '/'),
        secure = request.get('secure')
    ))

    ## return
    return Response(200, {
            "status": "success",
        }, set_cookie = {
            'name': 'simple_key',
            'value': 'simple_value',
            'http_only': request.get('http_only', False),
            'domain': request.get('domain'),
            'same_site': request.get('same_site'),
            'path': request.get('path', '/'),
            'secure': request.get('secure')
        }
    )
