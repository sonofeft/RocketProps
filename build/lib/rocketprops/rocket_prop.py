#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
RocketProps models liquid rocket propellants that are injected into liquid rocket chambers.

RocketProps calculates the various propellant properties required
to predict a liquid propellant thrust chamber's performance. 
This includes density, viscosity, vapor pressure,
heat of vaporization, surface tension, heat capacity and thermal conductivity. 
Other properties such as critical temperature and pressure, normal boiling point, 
molecular weight and freezing tempreature are available.


RocketProps
Copyright (C) 2020  Applied Python

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import os
here = os.path.abspath(os.path.dirname(__file__))


# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2020 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "4 - Beta" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

#
# import statements here. (built-in first, then 3rd party, then yours)
#
# Code goes below.
# Adjust docstrings to suite your taste/requirements.
#

class Propellant(object):
    """RocketProps models liquid rocket propellants that are injected into liquid rocket chambers.
    """

    def __init__(self):
        """Inits Propellants"""
        print('This is a place-holder for code to follow.')

if __name__ == '__main__':
    C = Propellant()
