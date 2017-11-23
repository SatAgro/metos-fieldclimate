# metos-fieldclimate

## Introduction

Python library to work with Metos FieldClimate meteorological stations JSON REST API. See [official documentation](http://www.fieldclimate.com/json_manual/json_manual.htm "Metos FieldClimte API documentation") for more information.

## Installation

By now, the repository is not available at pip but still, you can easily install the library directly from GitHub using pip by typing:

    pip install git+https://github.com/SatAgro/metos-fieldclimate.git


## Requirements

Python 2.7.9+ and 3.4.3+ should be compatible. Python 2 users need to install `enum34` from pypi.

## Usage

In order to use data from FieldClimate meteorological stations in your applications you must follow this steps:
  1. Get the data using FieldClimateRestAPI class
  2. Initialize a Station class with get JSON data from step 1.

Below you can find basic usage example.

    from FieldClimate import RestAPI
    from FieldClimate.Data import Station

    # Connect and get first station
    fc = RestAPI.FieldClimateRestAPI(YOUR_USER, YOUR_PASS)
    station_json = fc.get_stations()[0]

    # Get station sensor specification and data
    measures_json = fc.get_station_data_first(station_json['f_name'])
    sensors_json = fc.get_station_sensors(station_json['f_name'])

    # Initialize Station class and work with it
    station = Station(st, sens_st1, data_st1)

    precip_sensor = station.get_sensor('Precipitation')
    temp_sensor = station.get_sensor('Air temperature')
    measures = station.get_sensors_measures([precip_sensor, temp_sensor)

    # Export all sensors data to CSV file
    station.to_csv('test.csv', station.get_sensors())

## License

Krzysztof Stopa, Przemysław Żelazowski - SatAgro Project<br>
Phillip Marshall - Agrimanagement, Inc.

GNU LESSER GENERAL PUBLIC LICENSE Version 3
