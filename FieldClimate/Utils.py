__author__ = 'kstopa'

from RestAPI import FieldClimateRestAPI
from Data import Station, SensorMode
from datetime import datetime, timedelta

import sys

def get_station_data_date(user, password, station_name, date=datetime.now()):
    """

    :param user:
    :param passwd:
    :param station:
    :param date:
    :return:
    """
    fc = FieldClimateRestAPI(user, password)
    # Check stations
    st = fc.get_stations()
    station = None
    print("Getting data for stations:")
    print(st)
    for s in st:
        # Get all raw data for a station
        if station_name in s['f_name']:
            print('Station ok!')
            d_min = date.replace(hour=0, minute=0, second=0)
            d_max = date.replace(hour=23, minute=59, second=59)
            measures = fc.get_station_data_between_dates(s['f_name'], d_min, d_max)
            sensors = fc.get_station_sensors_statuses(station_name, d_min, d_max)
            station = Station(s, sensors, measures)
    # Process data: average temperature and cumulative precipitations
    if station:
        precip_sensor = station.get_sensor('Precipitation')
        temp_sensor = station.get_sensor('Air temperature')
        if temp_sensor is None or temp_sensor.get_status() is False:
            temp_sensor = station.get_sensor('HC Air temperature')
        temp_precip = station.get_sensors_measures([temp_sensor, precip_sensor])
        date_data = {'precipitation': get_sensor_sum(precip_sensor, temp_precip),
                     'temperature': {'aver': get_sensor_average(temp_sensor, temp_precip),
                                    'min': get_sensor_min(temp_sensor, temp_precip),
                                    'max': get_sensor_max(temp_sensor, temp_precip)}
        }
        return date_data
    else:
        print "No station found!"
        return None

def get_sensor_average(sensor_name, measures, mode=SensorMode.MODE_AVE):
    return round(get_sensor_sum(sensor_name, measures, mode)/ len(measures), 4)

def get_sensor_sum(sensor_name, measures, mode=SensorMode.MODE_SUM):
    m_sum = 0
    for m in measures:
        m_val = m.get_value(sensor_name, mode)
        if m_val:
            m_sum = m_sum + m_val
    return round(m_sum, 4)

def get_sensor_min(sensor_name, measures, mode=SensorMode.MODE_MIN):
    m_min = sys.float_info.max
    for m in measures:
        m_val = m.get_value(sensor_name, mode)
        if m_val and m_val < m_min:
            m_min = m_val
    return round(m_min, 4)

def get_sensor_max(sensor_name, measures, mode=SensorMode.MODE_MAX):
    m_max = sys.float_info.min
    for m in measures:
        m_val = m.get_value(sensor_name, mode)
        if m_val and m_val > m_max:
            m_max = m_val
    return round(m_max, 4)


if __name__ == '__main__':
    USER = sys.argv[1]
    PASS = sys.argv[2]
    data = get_station_data_date(USER, PASS, '0000027F', datetime.now() - timedelta(days=1))
    print data