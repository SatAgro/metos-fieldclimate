
import unittest
import datetime
import os
from FieldClimate import RestAPI

class TestMetosRestAPI(unittest.TestCase):

    METOS_USER = os.getenv('METOS_USER', '')
    METOS_PASSWORD = os.getenv('METOS_PASSWORD', '')

    def test_environment_setup(self):
        self.assertNotEqual(self.METOS_USER, '', "METOS_USER env variable must be set to perform the test.")
        self.assertNotEqual(self.METOS_PASSWORD, '', "METOS_PASSWORD env variable must be set to perform the test.")

    def test_stations(self):
        api = RestAPI.FieldClimateRestAPI(self.METOS_USER, self.METOS_PASSWORD)
        stations = api.get_stations()
        self.assertGreater(len(stations), 0, "Error getting stations.")
        for s in stations:
            sensors = api.get_station_sensors(s['f_name'])
            self.assertGreater(len(sensors), 1, "Station {0} has no sensors".format(s['f_name']))
            print(sensors)



if __name__ == '__main__':
    """
    Run the tests
    Note that METOS_USER and METOS_PASSWORD should be set to complete the tests
    """

    unittest.main()
