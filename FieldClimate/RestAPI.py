__author__ = "Krzysztof Stopa"
__copyright__ = "Copyright 2015 SatAgro"
__credits__ = ["Krzysztof Stopa", "Przemyslaw Zelazowski"]
__license__ = "LGPL"
__email__ = "buiro@satagro.pl"

import urllib
import urllib2
import json

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

    def get_station_data_next(self, station_name, rows=100, show_user_units=False, dt_from=datetime.now()):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
            'row_count': rows,
            'dt_from': dt_from.strftime('%Y-%m-%d %H:%M:%S'),
            'show_user_units': int(show_user_units)
        }

        return self.call_api_method('CIDIStationData/GetNext', params)['ReturnDataSet']

    def get_station_data_available_dates(self, station_name):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name,
        }

        return self.call_api_method('CIDIStationData/GetMinMaxDate', params)['ReturnDataSet']

    def get_station_all_data(self, station_name, rows=100, show_user_units=False):
        measures = []
        # Get min and max dates and get data each 100 rows.
        dts = self.get_station_data_available_dates(station_name)
        dt_min = datetime.strptime(dts['f_date_min'], '%Y-%m-%d %H:%M:%S')
        dt_max = datetime.strptime(dts['f_date_max'], '%Y-%m-%d %H:%M:%S')
        print('Data available from {0} to {1}'.format(dt_min.strftime('%Y-%m-%d %H:%M:%S'), dt_min.strftime('%Y-%m-%d %H:%M:%S')))
        dt_down = dt_min
        while dt_down < dt_max:
            print('Getting data from {0}'.format(dt_down.strftime('%Y-%m-%d %H:%M:%S')))
            ms = self.get_station_data_next(station_name, dt_from=dt_down)
            measures.append(ms)
            dt_down = datetime.strptime(ms[-1]['f_date'], '%Y-%m-%d %H:%M:%S')

        return measures

    def get_station_sensors(self, station_name):
        params = {
            'user_name': self.USER,
            'user_passw': self.PASS,
            'station_name': station_name
        }

        return self.call_api_method('CIDIStationSensors/Get', params)['ReturnDataSet']



