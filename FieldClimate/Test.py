import unittest
import os
import datetime
from FieldClimate.Api import FieldClimateRestAPI
from FieldClimate.Data import Station

class MetosTest(unittest.TestCase):

    METOS_USER = os.getenv('METOS_USER', '')
    METOS_PASSWORD = os.getenv('METOS_PASSWORD', '')

    def test_environment_setup(self):
        self.assertNotEqual(self.METOS_USER, '', "METOS_USER env variable must be set to perform the test.")
        self.assertNotEqual(self.METOS_PASSWORD, '', "METOS_PASSWORD env variable must be set to perform the test.")

    def test_stations(self):
        api = FieldClimateRestAPI(self.METOS_USER, self.METOS_PASSWORD, debug=True)
        stations = api.get_stations()
        self.assertGreater(len(stations), 0, "Error getting stations.")
        for s in stations:
            sensors = api.get_station_sensors(s['f_name'])
            self.assertGreater(len(sensors), 1, "Station {0} has no sensors".format(s['f_name']))

    def test_sensors(self):
        find_sensors = ['temperature', 'relative', 'precipitation', 'wind']
        api = FieldClimateRestAPI(self.METOS_USER, self.METOS_PASSWORD, debug=True)
        stations = api.get_stations()
        for s in stations:
            s_name = s['f_name']
            s_measures = api.get_station_data_first(s_name, rows=50)
            #get_station_all_data
            s_sensors = api.get_station_sensors(s_name)
            station = Station(s, s_sensors, s_measures)
            # Check if basic sensors are available
            for sensor in find_sensors:
                print(sensor)
                f_sensors = station.find_sensors(sensor)
                self.assertGreater(len(f_sensors), 0, 'Station {0} has no {1} sensors'.format(s_name, sensor))
                mss = station.get_sensors_measures(f_sensors)
                self.assertEqual(len(mss), 50, 'Missing {0} measures data. Expecting {1} and get {2} measures.'
                                 .format(sensor, 50, len(mss)))


if __name__ == '__main__':
    """
    Run the tests
    Note that METOS_USER and METOS_PASSWORD should be set to complete the tests
    """
    unittest.main()
