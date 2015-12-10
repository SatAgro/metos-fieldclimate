__author__ = 'kstopa'

from FieldClimate import RestAPI
from FieldClimate.Data import Station

if __name__ == '__main__':
    # Simple test and usage example.

    fc = RestAPI.FieldClimateRestAPI('lukaszkrechowiecki', 'cebulatfg')
    st = fc.get_stations()
    print(st)

    dates = fc.get_station_data_available_dates(st[0]['f_name'])

    mss = fc.get_station_all_data(st[0]['f_name'])
    print(mss)

    print(dates)

    data_st1 = fc.get_station_data_first(st[0]['f_name'])
    print("Data:")
    print(data_st1)

    sens_st1 = fc.get_station_sensors(st[0]['f_name'])
    print("Sensors:")
    print(sens_st1)

    station = Station(st, sens_st1, data_st1)

    precip_sensor = station.get_sensor('Precipitation')
    temp_sensor_0 = station.get_sensor('Air temperature')
    temp_sensor_1 = station.get_sensor('HC Air temperature')

    all_measures = station.get_sensors_measures([precip_sensor, temp_sensor_0, temp_sensor_1])

    for pm in all_measures:
        print pm


