
from chalice import Chalice, NotFoundError
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from chalicelib.blueprints import auth, dev
from chalicelib.config import cors, stage


app = Chalice(app_name='webstack')
app.register_blueprint(auth.blueprint, url_prefix='/auth')


## dev utilities
if stage in ['local', 'dev', 'beta']:
    from chalicelib.blueprints import dev
    app.register_blueprint(dev.blueprint, url_prefix='/dev')
