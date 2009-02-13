#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 José de Paula Eufrásio Júnior

#    This file is part of Crisk.
#
#    Crisk is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Crisk is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
import py2exe
import sys

sys.path.append('src/')

setup(
    name = 'crisk',
    description = 'Simple Risk Management Tool',
    version = '0.1',

    windows = [
                  {
                      'script': 'src/crisk.py',
                      'icon' : 'criskicon.ico'
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings, crisk, sqlalchemy.databases.sqlite',
                      'includes': 'cairo, pango, pangocairo, atk, gobject, geraldo, elixir',
                  }
              },

    data_files=[
                   ('glade', ['src/crisk/ui.glade']),
                   'src/COPYING'
               ]
)
