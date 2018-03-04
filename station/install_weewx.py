import sys
import traceback

from pexpect import spawn, EOF


CMD = 'bash -c "apt-get update && apt-get -y install weewx"'

LOCATION      = 'Hamilton, ON'
COORDS        = '43.257, -79.861'
ALTITUDE      = '2, meter'
UNITS         = 'Metric'
STATION_TYPE  = 'AcuRite'
STATION_MODEL = '02064M'


def main():
    try:
        child = spawn(CMD, timeout=60, encoding='utf-8')
        child.logfile = sys.stdout

        child.expect('location of the weather station')
        child.sendline(LOCATION)

        child.expect('latitude, longitude of the weather station')
        child.sendline(COORDS)

        child.expect('altitude of the weather station')
        child.sendline(ALTITUDE)

        child.expect('display units')
        child.sendline(UNITS)

        child.expect('weather station type')
        #  child.sendline(STATION_TYPE)
        child.sendline('Simulator')

        #  child.expect('weather station model')
        #  child.sendline(STATION_MODEL)

        child.expect(EOF)

    except:
        traceback.print_exc()

    finally:
        print('Closing child process')
        child.close()


if __name__ == '__main__':
    main()
