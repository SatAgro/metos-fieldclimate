#!/usr/bin/env python

# This file is part of Copernicus Atmosphere Monitoring Service (CAMS) downloading and
# processing tools (CAMS tools).

# CAMS tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or any later
# version.

# CAMS tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with CAMS tools.  If not, see <http://www.gnu.org/licenses/>.

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