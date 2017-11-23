#!/usr/bin/env python

from distutils.core import setup
import FieldClimate

setup(name='Metos Field Climate',
      version=FieldClimate.__version__,
      description='Pyton library to work with Metos FieldClimate meteo stations JSON REST API.',
      author=FieldClimate.__author__,
      author_email=FieldClimate.__email__,
      url='https://github.com/SatAgro/metos-fieldclimate',
      packages=['FieldClimate', 'Examples'],
    )