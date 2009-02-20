#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 José de Paula Eufrásio Júnior <jose.junior@gmail.com>

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
""" 
This is the basic package for the Crisk Application.
""" 

import sys
import os
from kiwi.environ import Application

# Adicionando paths para achar os resources

app = Application('crisk')
dir = os.path.dirname(__file__)
rdir = os.path.abspath(os.path.join(dir, '../../'))

if app.uninstalled:
#    app.add_global_resource('glade', os.path.join(rdir, 'glade'))
#    app.add_global_resource('pixmaps', os.path.join(rdir, 'pixmaps'))
    app.add_global_resource('glade', 'glade')
    app.add_global_resource('pixmaps', 'pixmaps')

app.enable_translation()
app.set_application_domain('crisk')

__url__ = 'http://coredump.github.com/crisk/'
__version__ = '0.2'
__license__ = """
Copyright 2009 José de Paula Eufrásio Júnior <jose.junior@gmail.com>

This file is part of Crisk.

Crisk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Crisk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
