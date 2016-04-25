__author__ = 'kstopa'

from RestAPI import FieldClimateRestAPI

def get_station_data_date(user, passwd, station, date):
    """

    :param user:
    :param passwd:
    :param station:
    :param date:
    :return:
    """
    fc = FieldClimateRestAPI(user, passwd)
    # Check stations
