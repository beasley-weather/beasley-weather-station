import json
import logging
import time
from os import environ as env
from traceback import print_exc
from typing import Dict
import datetime

import requests
from ..dbi import WeewxDB
from requests import HTTPError

from .consts import DEFAULT_INTERVAL
from .util import unix_time_to_human


SECS_IN_DAY = 24 * 3600


LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d ' \
                 '%(funcName)s > %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=LOGGING_FORMAT)
_logger = logging.getLogger(__name__)

class TransferClient:
    def __init__(self,
                 database_interfacer,
                 server_address,
                 interval=DEFAULT_INTERVAL,
                 interval_start_time=time.time() - SECS_IN_DAY,
                 *,
                 address_protocol='http'):
        '''
        :param database_interfacer:  An object that knows how to query the database
        :param server_send:          Function to send data to a server
        :param interval:             Transfer interval (seconds)
        :param interval_start_time:  Start of first interval (seconds since epoch)
        :param address_protocol:     If server_send does not specify a protocol,
           it can be overridden by specifying an address_protocol argument.
           (default: http)
        '''
        _logger.info('Interval start time: {} ({})'.format(
                       unix_time_to_human(interval_start_time),
                       round(interval_start_time)))

        self._is_running = True
        self._database_interfacer = database_interfacer
        if ('://' not in server_address):
            server_address = '{}://{}'.format(address_protocol, server_address)
        self._server_address = server_address
        self._interval = int(interval)
        self._last_query_time = interval_start_time

    def start(self):
        start_time = time.time()
        time_now = start_time

        def sleepUntilNextInterval():
            print()
            sleepTime = self._interval - (time_now - start_time) % self._interval
            _logger.info('Sleeping for {}s'.format(sleepTime))
            time.sleep(sleepTime)

        while self._is_running:
            try:
                data = self._load_last_interval_data(round(time_now))
            except IOError as exc:
                _logger.error('Unable to query data for the interval '
                              '({}, {}): {}'.format(
                                round(self._last_query_time), round(time_now), exc))

            try:
                self._transfer_data(data)
                sleepUntilNextInterval()
                self._last_query_time = time_now
            except IOError as exc:
                _logger.error('Unable to transfer data to {}: {}'.format(
                                self._server_address, exc))
                sleepUntilNextInterval()

            time_now = time.time()


    def stop(self):
        self._is_running = False

    def _load_last_interval_data(self, to: int) -> Dict:
        '''
        :to: End of interval
        :return:
        :raises: IOError if query fails
        '''
        from_ = max(to - SECS_IN_DAY, round(self._last_query_time))
        _logger.info('Querying data between {} ({}) and {} ({})'.format(
                       unix_time_to_human(from_), from_, unix_time_to_human(to), to))

        try:
            data = self._database_interfacer.archive_query_interval(from_, to)
        except IOError as exc:
            raise exc

        return json.dumps(data)

    def _transfer_data(self, data, tries = 3) -> None:
        '''
        :param data: Binary data
        :param tries: Number of attempt to transfer data before giving up
        :raise: IOError if unable to transfer data
        '''
        _logger.info('Transfering data of length {}'.format(len(data)))
        for i in range(1, 4):
            try:
                resp = requests.post(self._server_address, data=data)
                if not resp.ok:
                    resp.raise_for_status()
                return
            except HTTPError as exc:
                _logger.error('Unable to transfer data: {}'.format(exc))
            except requests.RequestException:
                print_exc()
            finally:
                waitSecs = i ** 3 * 2
                _logger.info('Will try again in {}s'.format(waitSecs))
                time.sleep(waitSecs)

        raise IOError('Unable to transfer data. {} attempts made.'.format(tries))


def create_client(server_address, database, interval, interval_start_time=None):
    '''
    :param server_address: Address for server
    :param database: Database name
    :param interval: Transfer interval
    :param interval_start_time:  Start of first interval (seconds since epoch)
    '''

    _logger.info('Creating client\n'
                 + 'Server: {}\n'.format(server_address)
                 + 'Database: {}\n'.format(database)
                 + 'Interval: {}'.format(interval))
    database_interfacer = WeewxDB(database)
    if interval_start_time is not None:
        return TransferClient(database_interfacer,
                              server_address,
                              interval,
                              interval_start_time)
    else:
        return TransferClient(database_interfacer,
                              server_address,
                              interval)


if __name__ == '__main__':
    client = create_client(env.get('DTS_SERVER'),
                           env.get('WEEWX_DATABASE') or '/var/lib/weewx/weewx.sdb',
                           env.get('DTS_INTERVAL') or 300)
    client.start()
