import json
from json import JSONDecodeError
import subprocess as sp
from traceback import print_exc

from ..dbi import WeewxDB
from flask import Flask, request


def create_app(database):
    """
    :param database: Name of database to save into
    """
    app = Flask(__name__)

    weewx_db = WeewxDB(database)

    @app.route('/', methods=['POST'])
    def route_data():
        try:
            data = json.loads(request.data.decode('utf-8'))
            weewx_db.archive_insert_data(data)
        except JSONDecodeError:
            print_exc()
            return 422, 'Invalid JSON'
        except IOError:
            print_exc()
            return 500, 'Unable to save data'

        rebuild_weewx_reports()

        return ''

    @app.route('/data', methods=['POST'])
    def route_data_deprecated():
        return 'This route, /data, is deprecated. Use / instead\n' + route_data()

    @app.route('/')
    def route_index():
        return 'yooo, what what!'

    return app


def rebuild_weewx_reports():
    proc = sp.run(['wee_reports'])
    if proc.returncode == 0:
        print('Successfully generated reports')
        return True
    else:
        print('Failed to generate reports')
        return False
