from __future__ import print_function

__author__ = "Krzysztof Stopa"
__copyright__ = "Copyright 2015 SatAgro"
__credits__ = ["Krzysztof Stopa", "Przemyslaw Zelazowski"]
__license__ = "LGPL"
__email__ = "buiro@satagro.pl"

import sys

from FieldClimate import RestAPI
from FieldClimate.Data import Station

if __name__ == '__main__':
    # Simple test and usage example.
    USER = sys.argv[1]
    PASS = sys.argv[2]
    fc = RestAPI.FieldClimateRestAPI(USER, PASS)
    st = fc.get_stations()
    print("Getting data for stations:")
    print(st)
    for s in st:
        # Get all raw data for a station
        print("Downloading data for {f_name} ({f_latitude}, {f_longitude})".format(**s))
        st_sensors = fc.get_station_sensors(s['f_name'])
        print("Available sensors")
        print(st_sensors)
        print("Downloading measures...")
        st_measures = fc.get_station_all_data(s['f_name'])  # fc.get_station_data_last(s['f_name'])
        # create station
        station = Station(s, st_sensors, st_measures)
        for i in station.get_sensors():
            print(str(i))
        # Get processed data
        precip_sensor = station.get_sensor('Precipitation')
        temp_sensor_0 = station.get_sensor('Air temperature')
        if temp_sensor_0 is None:
            temp_sensor_0 = station.get_sensor('Soil temperature')
        if temp_sensor_0 is None:
            temp_sensor_0 = station.get_sensor('HC Air temperature')
        temp_sensor_1 = station.get_sensor('HC Air temperature')
        # Export data
        print("Exporting data to {f_name}_{f_latitude}_{f_longitude}.csv".format(**s))
        station.to_csv("{f_name}_{f_latitude}_{f_longitude}.csv".format(**s),
                       [precip_sensor, temp_sensor_0, temp_sensor_1])
