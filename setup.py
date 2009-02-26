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
import glob

if os.name in ['win32', 'windows', 'nt']:
    import py2exe

depends = ['geraldo', 'kiwi', 'elixir', 'reportlab', 'matplotlib', 'pygtk']

for mod in depends:
    try:
        __import__(mod)
    except ImportError:
        raise SystemError('Module %s on the latest version is required to run crisk.' % mod)

sys.path.append('./src')
import crisk
import matplotlib
        
from kiwi.dist import listfiles, listpackages, setup

if os.name in ['win32', 'windows', 'nt']:
    data_files = [
        ('pixmaps',
         listfiles('pixmaps', '*.*')),
        ('glade',
         listfiles('glade', '*.glade')),
        ('locale/pt_BR/LC_MESSAGES', 
          [ 'locale/pt_BR/LC_MESSAGES/crisk.mo' ] ),
        ('doc/crisk', 
          listfiles('docs', '*')),
        ]
    
#    data_files.append(mpl_datafiles)
    data_files.extend(matplotlib.get_py2exe_datafiles())
    
    global_resources = dict(
        pixmaps='pixmaps',
        glade='glade',
        locale='locale'
        )

    resources = dict(
        locale = 'locale',
        basedir = '.')

    
else:
    data_files = [
        ('$datadir/pixmaps',
         listfiles('pixmaps', '*.*')),
        ('$datadir/glade',
         listfiles('glade', '*.glade')),
        ('share/locale/pt_BR/LC_MESSAGES', 
          [ 'locale/pt_BR/LC_MESSAGES/crisk.mo' ] ),
        ('share/doc/crisk', 
          listfiles('docs', '*')),
        ]

    global_resources = dict(
        pixmaps='$datadir/pixmaps',
        glade='$datadir/glade',
        docs='$prefix/share/doc/crisk'
        )

    resources = dict(
        locale = '$prefix/share/locale',
        basedir = '$prefix')

packages = ['crisk', 'crisk.reports']

package_dir = {'crisk' : 'src/crisk', 
               'crisk.reports' : 'src/crisk/reports'}

scripts = [
               'src/crisk.py'
          ]

setup(
    name = 'crisk',
    description = crisk.__shortdescription__,
    version = crisk.__version__,
    author = crisk.__author__,
    author_email = 'jose.junior@gmail.com',
    long_description = crisk.__description__,
    url = crisk.__url__,
    license = 'GNU GPLv3 (see COPYING)',
    
    packages = packages,
    package_dir = package_dir,
    scripts = scripts,
    data_files = data_files,
    global_resources = global_resources,
    resources = resources,
    
    windows = [
                  {
                      'script': 'src/crisk.py',
                      'icon' : 'criskicon.ico'
                  }
              ],

    options = {
                  'py2exe': {
                      'packages' : ['encodings', 'crisk', 'sqlalchemy.databases.sqlite',
                                    'locale', 'gettext'  
                                   ],
                      
                      'includes': [ 'cairo', 'pango', 'pangocairo', 'atk', 'gobject', 
                                   'geraldo', 'elixir', 'matplotlib', 'pytz', 'pylab', 
                                   'matplotlib.numerix.random_array', 'matplotlib.backends',
                                   'matplotlib.backends.backend_agg'
                                   ]
                      
                  }
              }
)
