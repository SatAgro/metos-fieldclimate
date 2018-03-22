from __future__ import print_function

__author__ = "Krzysztof Stopa"
__copyright__ = "Copyright 2015 SatAgro"
__credits__ = ["Krzysztof Stopa", "Przemyslaw Zelazowski", "Phillip Marshall"]
__license__ = "LGPL"
__email__ = "buiro@satagro.pl"

import json
import ssl
from datetime import datetime

try:
    # Python 2:
    from urllib import urlencode
    from urllib2 import urlopen
except ImportError:
    # Python 3:
    from urllib.parse import urlencode
    from urllib.request import urlopen


class RestAPI(object):
    API_URL = None
    DEBUG = False
    context = None

    def __init__(self, url, debug=False):
        self.API_URL = url
        self.DEBUG = debug

    def call_api_method(self, method, params):
        url = self.API_URL + method
        params = urlencode(params).encode('ascii')
        # Read url and parse from json
        # Note: The context argument was added in Python 2.7.9 and 3.4.3
        request = urlopen(url, params, context=self.context).read().decode('utf8')
        return json.loads(request)


class FieldClimateRestAPI(RestAPI):
    USER = None
    PASS = None
    CHUNK_SIZE = 100

    def __init__(self, user, passwd, https=False, debug=False):
        if https:
            # Warning: Fieldclimate's certificate doesn't seem to validate.
            # This workaround disables cert verification, but keeps TLS encryption.
            url = 'https://www.fieldclimate.com/api/'
            self.gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        else:
            url = 'http://www.fieldclimate.com/api/'
        super(FieldClimateRestAPI, self).__init__(url, debug)
        self.USER = user
        self.PASS = passwd

    def auth_params(self, more=None):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS
        }
        if more is not None:
            params.update(more)
        return params

    def get_stations(self):
        params = self.auth_params({
            'row_count': 5000  # todo: resolve case for >5000 stations
        })
        return self.call_api_method('CIDIStationList/GetFirst', params)['ReturnDataSet']

    def get_station(self, station_name):
        # todo: It would be more efficient to ask the server for just one station,
        # but there doesn't seem to be an API method for this use case.
        for station in self.get_stations():
            if station['f_name'] == station_name:
                return station
        # Station not found
        return None

    def get_station_config(self, station_name):
        params = self.auth_params({
            'station_name': station_name
        })
        return self.call_api_method('CIDIStationConfig2/Get', params)['ReturnDataSet'][0]

    def get_station_data_last(self, station_name, rows=None, group=None, show_user_units=False):
        params = self.auth_params({
            'station_name': station_name,
            'row_count': rows or self.CHUNK_SIZE,
            'show_user_units': int(show_user_units)
        })
        if group is not None:
            params.update({'group_code': group})
        req = self.call_api_method('CIDIStationData/GetLast', params)
        if 'ReturnDataSet' in req:
            return req['ReturnDataSet']
        else:
            if self.DEBUG:
                print(req)
            return req

    def get_station_data_first(self, station_name, rows=None, group=None, show_user_units=False):
        params = self.auth_params({
            'station_name': station_name,
            'row_count': rows or self.CHUNK_SIZE,
            'show_user_units': int(show_user_units)
        })
        if group is not None:
            params.update({'group_code': group})
        return self.call_api_method('CIDIStationData/GetFirst', params)['ReturnDataSet']

    def get_station_data_next(self, station_name, rows=None, group=None, show_user_units=False, dt_to=None):
        if dt_to is None:
            dt_to = datetime.now()
        params = self.auth_params({
            'station_name': station_name,
            'row_count': rows or self.CHUNK_SIZE,
            'dt_from': dt_to.strftime('%Y-%m-%d %H:%M:%S'),
            'show_user_units': int(show_user_units)
        })
        if group is not None:
            params.update({'group_code': group})
        return self.call_api_method('CIDIStationData/GetNext', params)['ReturnDataSet']

    def get_station_data_from_date(self, station_name, rows=None, group=None, show_user_units=False, dt_from=None):
        if dt_from is None:
            dt_from = datetime.now()
        params = self.auth_params({
            'station_name': station_name,
            'row_count': rows or self.CHUNK_SIZE,
            'dt_from': dt_from.strftime('%Y-%m-%d %H:%M:%S'),
            'show_user_units': int(show_user_units)
        })
        if group is not None:
            params.update({'group_code': group})
        return self.call_api_method('CIDIStationData/GetFromDate', params)['ReturnDataSet']

    def get_station_data_available_dates(self, station_name):
        params = self.auth_params({
            'station_name': station_name,
        })
        return self.call_api_method('CIDIStationData/GetMinMaxDate', params)['ReturnDataSet']

    def get_station_data_between_dates(self, station_name, date_min, date_max=None, group=None, show_user_units=False):
        if date_max is None:
            date_max = datetime.now()
        measures = []
        # Get min and max dates and get data each 100 rows.
        if self.DEBUG:
            print('Getting data from {0} to {1}'.format(date_min.strftime('%Y-%m-%d %H:%M:%S'),
                                                        date_max.strftime('%Y-%m-%d %H:%M:%S')))
        date_down = date_min
        while date_down < date_max:
            ms = self.get_station_data_from_date(station_name, group=group, show_user_units=show_user_units,
                                                 dt_from=date_down)
            if not date_min == date_down:
                ms.pop(0)  # Pop first element due to it is te last of previous call.
            for m in ms:
                if date_max > datetime.strptime(m['f_date'], '%Y-%m-%d %H:%M:%S'):
                    measures.append(m)
            if ms:
                date_down = datetime.strptime(ms[-1]['f_date'], '%Y-%m-%d %H:%M:%S')
            else:
                # When using group, date_max will never be reached. So stop if zero rows are returned.
                date_down = date_max
        return measures

    def get_station_all_data(self, station_name, group=None, show_user_units=False):
        # Get min and max dates and get data each 100 rows.
        dates = self.get_station_data_available_dates(station_name)
        date_min = datetime.strptime(dates['f_date_min'], '%Y-%m-%d %H:%M:%S')
        date_max = datetime.strptime(dates['f_date_max'], '%Y-%m-%d %H:%M:%S')
        return self.get_station_data_between_dates(station_name, date_min, date_max, group=group,
                                                   show_user_units=show_user_units)

    def get_station_sensors(self, station_name):
        params = self.auth_params({
            'station_name': station_name
        })
        return self.call_api_method('CIDIStationSensors/Get', params)['ReturnDataSet']

    def get_station_sensors_statuses(self, station_name, dt_from, dt_to=datetime.now()):
        params = self.auth_params({
            'station_name': station_name,
            'dt_from': dt_from.strftime('%Y-%m-%d'),
            'dt_to': dt_to.strftime('%Y-%m-%d')
        })
        return self.call_api_method('CIDIStationSensors/GetSensorsStatuses', params)['ReturnDataSet']
