from chalice import Chalice, NotFoundError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

app = Chalice(app_name='webstack')

OBJECTS = {}


@app.route('/test', methods=['GET'], cors=True)
def GET_test():
    return {'key': 'value'}


@app.route('/objects/{key}', methods=['GET', 'PUT'], cors=True)
def GET_myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)


@app.route('/products', methods=['GET'], cors=True)
def GET_products():
    scope = ['https://spreadsheets.google.com/feeds']
    SPREADSHEET_KEY = '1c919wtwvSx_tbBcIVXO4DLF5nwxsjH7pHTIfQa8u3Ao'
    RANGE = 'Inventory!A1:E'

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'vendor/credentials.json',
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

    # sheets = Sheets.from_files('vendor/client_secrets.json', 'storage.json')
    # print(sheets)
    # sheet = sheets['1c919wtwvSx_tbBcIVXO4DLF5nwxsjH7pHTIfQa8u3Ao']
    # print(sheet)
    # tab = sheet.find('Inventory')
    # print(tab)
    # print(tab['A1'])
    # return str(tab)
