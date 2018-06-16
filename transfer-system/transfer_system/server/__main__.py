# TODO
# - logging

from os import environ as env

from .app import create_app

print('Starting transfer server')

app = create_app(env['WEEWX_DATABASE'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(env['DTS_PORT']))
