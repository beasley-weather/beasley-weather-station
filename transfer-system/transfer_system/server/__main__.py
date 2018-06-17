from os import environ as env

from .app import create_app


app = create_app(env.get('WEEWX_DATABASE') or '/var/lib/weewx/weewx.sdb')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(env['DTS_PORT']) or 5000)
