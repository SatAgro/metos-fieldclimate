__author__ = "Krzysztof Stopa"
__copyright__ = "Copyright 2015 SatAgro"
__credits__ = ["Krzysztof Stopa", "Przemyslaw Zelazowski"]
__license__ = "LGPL"
__email__ = "buiro@satagro.pl"

from datetime import datetime
import csv

__author__ = 'kstopa'

class Station():

    props = None
    sensors = None
    measures = None

    def __init__(self, properties, sensors, measures):
        self.pros = properties
        self.sensors = sensors
        self.measures = measures

    def get_name(self):
        return self.props['f_name']

    def get_user_name(self):
        if self.props['f_user_name'] is not None:
            return self.props['f_user_name']
        elif self.props['f_custom_name'] is not None:
            return self.props['f_custom_name']
        else:
            return None

    def get_latitude(self):
        return self.props['f_latitude']

    def get_longitude(self):
        return self.props['f_longitude']

    def get_sensor(self, sensor_name):
        for s in self.sensors:
            if s['f_name'] == sensor_name:
                return Sensor(s)
        return None

    def get_sensors(self):
        sensors = []
        for s in self.sensors:
            sensors.append(Sensor(s))
        return sensors

    def get_sensors_measures(self, sensors):
        measures = []
        for m in self.measures:
            sm = Measure(m['f_date'])
            for s in sensors:
                for mode in s.get_modes():
                    sm.add_value(m[s.get_measure_id(mode)])

            measures.append(sm)
        return measures

    def get_sensors_measures_header(self, sensors):
        header = ['f_date']
        for s in sensors:
            for mode in s.get_modes():
                header.append(s.get_name() + '_' + s.get_measure_id(mode))
        return header

    def to_csv(self, csv_path, sensors, delimiter=';'):
        with open(csv_path, 'wb') as csv_file:
            st_data = csv.writer(csv_file, delimiter=delimiter)
            header = self.get_sensors_measures_header(sensors)
            measures = self.get_sensors_measures(sensors)
            st_data.writerow(header)
            for m in measures:
                st_data.writerow([m.date] + m.values)


class Sensor():

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
        :param type: measure type (aver|min|max)
        :return: sens_type_code_channel
        """
        return 'sens_{0}_{1}_{2}'.format(mode, self.get_channel(), self.get_code())

    def get_modes(self):
        modes = []
        if int(self.props['f_val_sum']) == 1:
            modes.append('sum')
        if int(self.props['f_val_aver']) == 1:
            modes.append('aver')
        if int(self.props['f_val_min']) == 1:
            modes.append('min')
        if int(self.props['f_val_max']) == 1:
            modes.append('max')
        return modes

    def get_name(self):
        return self.props['f_name']

    def get_units(self):
        return self.props['f_units']


class Measure():
    date = None
    values = []

    def __init__(self, date_txt):
        self.values = []
        self.date = datetime.strptime(date_txt, "%Y-%m-%d %H:%M:%S")

    def add_value(self, value):
        self.values.append(value)

    def __str__(self):
        str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        for v in self.values:
            str += ';{0}'.format(v)
        return str
