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
#    along with Crisk.  If not, see <http://www.gnu.org/licenses/>.

from kiwi.ui.delegates import ProxySlaveDelegate

from model import *

class BasicsView(ProxySlaveDelegate):
    def __init__(self):        
        widget_list = ['name', 'location', 'initial_date', 'scope']
        try:
            basics_model = Basic.get(1)
        except:
            basics_model = None
            
        ProxySlaveDelegate.__init__(self, basics_model, widget_list, 
                                    gladefile = 'ui', 
                                    toplevel_name = 'BasicsWindow')
    def proxy_updated(self, *args):
#        print args
#        session.commit()
        pass