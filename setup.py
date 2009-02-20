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


import os
import sys
if os.name == 'win32':
    import py2exe

depends = ['geraldo', 'kiwi', 'elixir', 'reportlab', 'matplotlib', 'pygtk']

for mod in depends:
    try:
        __import__(mod)
    except ImportError:
        raise SystemError('Module %s on the latest version is required to run crisk.' % mod)
        
from kiwi.dist import listfiles, listpackages, setup

data_files = [
    ('$datadir/pixmaps',
     listfiles('pixmaps', '*.*')),
    ('$datadir/glade',
     listfiles('glade', '*.glade')),
    ('share/doc/crisk',
     ['src/COPYING', 'src/README'])]

#resources = dict(
#    locale='$prefix/share/locale',
#    basedir='$prefix')

global_resources = dict(
    pixmaps='$datadir/pixmaps',
    glade='$datadir/glade',
    docs='$prefix/share/doc/stoq',
    locale = '$prefix/share/locale')

packages = ['crisk', 'crisk.reports']
package_dir = {'crisk' : 'src/crisk', 
               'crisk.reports' : 'src/crisk/reports'}

scripts = [
               'src/crisk.py'
          ]

setup(
    name = 'crisk',
    description = 'Simple Risk Management Tool',
    version = '0.3',
    author = 'José de Paula E. Júnior (coredump)',
    author_email = 'jose.junior@gmail.com',
    long_description = """
    Crisk is a simple tool for Risk Management, aimed at security officers,
    security consultants and risk professionals.
    """,
    url = 'http://coredump.github.com/crisk',
    license = 'GNU GPLv3 (see COPYING)',
    
    packages = packages,
    package_dir = package_dir,
    scripts = scripts,
    data_files = data_files,
#    resources = resources,
    global_resources = global_resources,
    
    windows = [
                  {
                      'script': 'src/crisk.py',
                      'icon' : 'criskicon.ico'
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings, crisk, sqlalchemy.databases.sqlite',
                      'includes': 'cairo, pango, pangocairo, atk, gobject, geraldo, elixir, matplotlib',
                  }
              }
)
