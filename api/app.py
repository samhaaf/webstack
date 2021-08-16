
from chalice import Chalice, NotFoundError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from chalicelib.orm.users import User
from chalicelib.blueprints import auth
from chalicelib.config import cors


app = Chalice(app_name='webstack')
app.register_blueprint(auth.blueprint)

OBJECTS = {}


@app.route('/test', methods=['GET'], cors=cors)
def GET_test():
    return {'key': 'value'}


@app.route('/objects/{key}', methods=['GET', 'PUT'], cors=cors)
def GET_myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)


@app.route('/products', methods=['GET'], cors=cors)
def GET_products():
    scope = ['https://spreadsheets.google.com/feeds']
    SPREADSHEET_KEY = '1c919wtwvSx_tbBcIVXO4DLF5nwxsjH7pHTIfQa8u3Ao'
    RANGE = 'Inventory!A1:E'

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'chalicelib/vendor/credentials.json',
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
