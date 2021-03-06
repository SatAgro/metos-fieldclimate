# metos-fieldclimate

## Deprecation warning

Since December 1st, 2018 old FieldClimate API run out of service and is no longer be available. So this library is no longer usable and we encourge you to switch to one of bellow listed options:

* https://github.com/agrimgt/python-fieldclimate (recommended)
* https://github.com/SatAgro/fieldclimate

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

    from FieldClimate.Api import FieldClimateRestAPI
    from FieldClimate.Data import Station

    # Connect and get first station
    fc = FieldClimateRestAPI(YOUR_USER, YOUR_PASS)
    station_json = fc.get_stations()[0]

    # Get station sensor specification and data
    sensors_json = fc.get_station_sensors(station_json['f_name'])
    measures_json = fc.get_station_data_first(station_json['f_name'])
    

    # Initialize Station class and work with it
    station = Station(station_json, sensors_json, measures_json)

    precip_sensor = station.get_sensor('Precipitation')
    temp_sensor = station.get_sensor('Air temperature')
    measures = station.get_sensors_measures([precip_sensor, temp_sensor)

    # Export all sensors data to CSV file
    station.to_csv('test.csv', station.get_sensors())

## Testing

Simple unit tests have been added to check the proper installation and basic 
functionality of the library. To run it just type:

    python Test.py

## License

Krzysztof Stopa, Przemysław Żelazowski - SatAgro Sp. z o.o.
Phillip Marshall - Agrimanagement, Inc.
Denis Voronin

GNU LESSER GENERAL PUBLIC LICENSE Version 3
