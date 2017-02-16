from __future__ import print_function

__author__ = "Krzysztof Stopa"
__copyright__ = "Copyright 2015 SatAgro"
__credits__ = ["Krzysztof Stopa", "Przemyslaw Zelazowski"]
__license__ = "LGPL"
__email__ = "buiro@satagro.pl"

import json
import ssl
import urllib
import urllib2
from datetime import datetime


class RestAPI():

    APIURL = None

    def __init__(self, url):
        self.API_URL = url

    def call_api_method(self, method, params):

        url = self.API_URL + method
        params = urllib.urlencode(params)
        # Read url and parse from json
        return json.loads(urllib2.urlopen(url, params).read())


class FieldClimateRestAPI(RestAPI):

    USER = None
    PASS = None

    def __init__(self, user, passwd):

        RestAPI.__init__(self, 'http://www.fieldclimate.com/api/')
        self.USER = user
        self.PASS = passwd

    def get_stations(self):

        params = {
            'user_name': self.USER,
            'user_passw': self.PASS
        }

        return self.call_api_method('CIDIStationList/GetFirst', params)['ReturnDataSet']

    def get_station_data_last(self, station_name, rows=100, show_user_units=False):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
            'row_count': rows,
            'show_user_units': int(show_user_units)
        }
        req = self.call_api_method('CIDIStationData/GetLast', params)
        if 'ReturnDataSet' in req:
            return req['ReturnDataSet']
        else:
            print(req)
            return req

    def get_station_data_first(self, station_name, rows=100, show_user_units=False):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
            'row_count': rows,
            'show_user_units': int(show_user_units)
        }

        return self.call_api_method('CIDIStationData/GetFirst', params)['ReturnDataSet']

    def get_station_data_next(self, station_name, rows=100, show_user_units=False, dt_to=datetime.now()):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
            'row_count': rows,
            'dt_from': dt_to.strftime('%Y-%m-%d %H:%M:%S'),
            'show_user_units': int(show_user_units)
        }

        return self.call_api_method('CIDIStationData/GetNext', params)['ReturnDataSet']

    def get_station_data_from_date(self, station_name, rows=100, show_user_units=False, dt_from=datetime.now()):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
            'row_count': rows,
            'dt_from': dt_from.strftime('%Y-%m-%d %H:%M:%S'),
            'show_user_units': int(show_user_units)
        }

        return self.call_api_method('CIDIStationData/GetFromDate', params)['ReturnDataSet']

    def get_station_data_available_dates(self, station_name):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
        }

        return self.call_api_method('CIDIStationData/GetMinMaxDate', params)['ReturnDataSet']

    def get_station_data_between_dates(self, station_name, date_min, date_max=datetime.now()):
        measures = []
        # Get min and max dates and get data each 100 rows.
        print('Getting data from {0} to {1}'.format(date_min.strftime('%Y-%m-%d %H:%M:%S'), date_max.strftime('%Y-%m-%d %H:%M:%S')))
        date_down = date_min
        while date_down < date_max:
            ms = self.get_station_data_from_date(station_name, dt_from=date_down)
            if not date_min == date_down:
                ms.pop(0)   # Pop first element due to it is te last of previous call.
            for m in ms:
                if date_max > datetime.strptime(m['f_date'], '%Y-%m-%d %H:%M:%S'):
                    measures.append(m)
            date_down = datetime.strptime(ms[-1]['f_date'], '%Y-%m-%d %H:%M:%S')
        return measures

    def get_station_all_data(self, station_name):
        measures = []
        # Get min and max dates and get data each 100 rows.
        dates = self.get_station_data_available_dates(station_name)
        date_min = datetime.strptime(dates['f_date_min'], '%Y-%m-%d %H:%M:%S')
        date_max = datetime.strptime(dates['f_date_max'], '%Y-%m-%d %H:%M:%S')
        return self.get_station_data_between_dates(station_name, date_min, date_max)

    def get_station_sensors(self, station_name):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name
        }

        return self.call_api_method('CIDIStationSensors/Get', params)['ReturnDataSet']

    def get_station_sensors_statuses(self, station_name, dt_from, dt_to=datetime.now()):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
            'dt_from': dt_from.strftime('%Y-%m-%d'),
            'dt_to':  dt_to.strftime('%Y-%m-%d')
        }

        return self.call_api_method('CIDIStationSensors/GetSensorsStatuses', params)['ReturnDataSet']

