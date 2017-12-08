from __future__ import print_function

__author__ = "Krzysztof Stopa"
__copyright__ = "Copyright 2015 SatAgro"
__credits__ = ["Krzysztof Stopa", "Przemyslaw Zelazowski", "Phillip Marshall"]
__license__ = "LGPL"
__email__ = "buiro@satagro.pl"

import csv
from datetime import datetime
from enum import Enum


class Station(object):
    props = None
    sensors = None
    measures = None

    def __init__(self, properties, sensors, measures):
        self.props = properties
        self.sensors = sensors
        self.measures = measures

    def get_uid(self):
        return self.props['f_uid']

    def get_name(self):
        return self.props['f_name']

    def get_name_user(self):
        return self.props['f_user_station_name']

    def get_user_name(self):
        if self.props['f_user_name'] is not None:
            return self.props['f_user_name']
        elif self.props['f_custom_name'] is not None:
            return self.props['f_custom_name']
        else:
            return None

    def get_latitude(self):
        return float(self.props['f_latitude'])

    def get_longitude(self):
        return float(self.props['f_longitude'])

    def get_sensor(self, sensor_name):
        """
        Get a sensor by its name.
        :param sensor_name: Sensor name located at s['f_name'] of the json response.
        :return: a Sensor or None if sensor does not exists.
        """
        for s in self.sensors:
            if s['f_name'] == sensor_name:
                return Sensor(s)
        return None

    def find_sensors(self, sensor_name):
        """
        Find sensor that contains sensor_name in its name. Not case sensitive.
        :param sensor_name: 
        :return: 
        """
        sensors = []
        sn = sensor_name.lower()
        for s in self.sensors:
            if sn in s['f_name'].lower():
                sensors.append(Sensor(s))
        return sensors

    def get_sensors(self):
        """
        Get all sensors of given station.
        :return: A list of Sensors
        """
        sensors = []
        for s in self.sensors:
            sensors.append(Sensor(s))
        return sensors

    def get_sensors_measures(self, sensors, sens_date=None):
        """ 
        Get all measures a given sensors and optionally at given date.
        """
        mss = []
        if sens_date:
            fmt_date = sens_date.strftime('%Y-%m-%d')
        for m in self.measures:
            if not sens_date or fmt_date in m['f_date']:
                sm = Measure(m['f_date'])
                for s in sensors:
                    for mode in s.get_modes():
                        sm.add_value(s.get_name(), mode, m[s.get_measure_id(mode)])
                mss.append(sm)
        return mss

    def get_sensors_measures_header(self, sensors):
        header = ['Date']
        for s in sensors:
            for mode in s.get_modes():
                header.append(s.get_name() + '_' + s.get_measure_id(mode))
        return header


    def to_csv(self, csv_path, sensors, delimiter=';'):
        with open(csv_path, 'w') as csv_file:
            st_data = csv.writer(csv_file, delimiter=delimiter)
            header = self.get_sensors_measures_header(sensors)
            measures = self.get_sensors_measures(sensors)
            st_data.writerow(header)
            for m in measures:
                st_data.writerow([m.date] + m.get_values())


class SensorMode(Enum):
    MODE_MIN = "min"
    MODE_MAX = "max"
    MODE_AVE = "aver"
    MODE_SUM = "sum"

    def __str__(self):
        return self.value


class Sensor(object):
    props = None

    def __init__(self, properties):
        self.props = properties

    def get_channel(self):
        """ Get sensor connection chanel id
        :return: Chanel id
        """
        return int(self.props['f_sensor_ch'])

    def get_code(self):
        return int(self.props['f_sensor_code'])

    def get_measure_id(self, mode):
        """  Get code to access to a sensor average measure
        :param mode: measure type (aver|min|max|sum)
        :return: sens_type_code_channel
        """
        return 'sens_{0}_{1}_{2}'.format(mode, self.get_channel(), self.get_code())

    def get_modes(self):
        modes = []
        if int(self.props['f_val_sum']) == 1:
            modes.append(SensorMode.MODE_SUM)
        if int(self.props['f_val_aver']) == 1:
            modes.append(SensorMode.MODE_AVE)
        if int(self.props['f_val_min']) == 1:
            modes.append(SensorMode.MODE_MIN)
        if int(self.props['f_val_max']) == 1:
            modes.append(SensorMode.MODE_MAX)
        return modes

    def get_name(self):
        return self.props['f_name']

    def get_units(self):
        return self.props['f_units']

    def get_status(self):
        """
        Get the status of the station. In order to have this data you must to load station sensor information with
        get_station_sensor_statuses from RestAPI.
        :return: True or false. If no status information has been loaded by defualt true.
        """
        if 'f_sensor_status' in self.props:
            print(self.props['f_sensor_status'])
            return bool(self.props['f_sensor_status'])
        else:
            return True

    def __str__(self):
        return self.get_name()

    def __unicode__(self):
        return self.get_name()


class Measure(object):
    date = None
    data = {}
    delimiter = ';'

    def __init__(self, date_txt):
        self.data = {}
        self.date = datetime.strptime(date_txt, "%Y-%m-%d %H:%M:%S")

    def add_value(self, sensor, mode, value):
        if sensor not in self.data:
            self.data[sensor] = {}
        if value:
            self.data[sensor][mode] = round(float(value), 2)


    def get_values(self):
        values = []
        for s in self.data:
            for m in self.data[s]:
                values.append(self.data[s][m])
        return values

    def get_value(self, sensor, mode):
        if sensor in self.data:
            if mode in self.data[sensor]:
                return self.data[sensor][mode]
            else:
                return None
        else:
            return None

    def __str__(self):
        str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        for v in self.get_values():
            str += '{0}{1}'.format(self.delimiter, v)
        return str
