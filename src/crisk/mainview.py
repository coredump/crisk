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

import gtk
import pygtk
import sys, os
import kiwi.environ

from elixir import *
from os import path
from kiwi.ui.dialogs import error, warning, yesno, save, messagedialog
from kiwi.ui.dialogs import open as open_dialog
from kiwi.ui.objectlist import Column, ObjectList
from kiwi.currency import currency
from kiwi.ui.widgets import textview, label, entry
from kiwi.ui.delegates import GladeDelegate, GladeSlaveDelegate, ProxySlaveDelegate

# Pedacos do programa

import crisk
from model import *
from basicsview import BasicsView
from inventoryview import InventoryView
from vulnerabilitiesview import VulnerabilitiesView
from reportview import ReportView

# Adicionando paths para achar os resources

if not hasattr(sys, 'frozen'):
    cwd = os.getcwd()
    standalone_path = os.path.join(cwd, 'crisk')
    kiwi.environ.environ.add_resource('glade', standalone_path)

class Step:
    def __init__(self, name, idx):
        self.name = name
        self.idx = idx        
        
class MainView(GladeDelegate):
    
    db_file = None

    def __init__(self):
       
        # Criando a tree inicial

        GladeDelegate.__init__(self, "ui", toplevel_name = 'MainWindow', 
                               delete_handler = self.on_exit__activate)        
        self.tree = self.get_widget('maintree')        
        tree = self.tree
        cols =  [ Column('name', title='Step', data_type = str, expand = True) ]
        tree.set_columns(cols)
        tree.set_headers_visible(False)
        basics = tree.append(None, Step('Basic Data', 0))
        first = tree.append(basics, Step('Target Information', 1))
        self.first = first
        tree.append(basics, Step('Inventory', 2))
        tree.append(basics, Step('Vulnerabilities', 3))
        tree.expand(basics)
        reports = tree.append(None, Step('Results', 4))
        self.first_report = tree.append(reports, Step('Inventory Report', 5))
        tree.expand(reports)
#        tree.select(self.first)

        if self.db_file is None:
            self.open_or_new()   
    
    def open_or_new(self):
        result = yesno('Do you want to open a previous file?\n\n' + 
                       'Choose \'Yes\' to open a previous work, or\n' + 
                       'choose \'No\' if you want to create a new DB') 
        if result == gtk.RESPONSE_YES:
            res = self.on_open__activate()
            if res is None:
                sys.exit()
        elif result == gtk.RESPONSE_NO:
            res = self.on_new__activate()
            if res is None:
                sys.exit()
        else:
            sys.exit()
    
    def check_and_detach(self):
        if self.get_slave('placeholder') is not None:
            self.detach_slave('placeholder')
    
    def on_maintree__selection_changed(self, *args):
        tree, step = args
        self.check_and_detach()
        index = step.idx
        if index == 0:
            tree.select(self.first)
        if index == 1:
            slave = BasicsView() 
            self.attach_slave('placeholder', slave)
        if index == 2:
            slave = InventoryView(parent = self)
            self.attach_slave('placeholder', slave)
        if index == 3:
            slave = VulnerabilitiesView(parent = self)
            self.attach_slave('placeholder', slave)
        if index == 4:
            tree.select(self.first_report)
        if index == 5:
            slave = ReportView(parent = self, reptype = 'inventory')
            self.attach_slave('placeholder', slave)  
                        
    def on_about__activate(self, *args):
        diag = gtk.AboutDialog()
        diag.set_name('Crisk')
        diag.set_version(crisk.__version__)
        diag.set_copyright('Copyright 2009 - José de Paula E. Júnior')
        diag.set_authors(['José de Paula E. Júnior <jose.junior@gmail.com>'])
        diag.set_comments('A simple risk management tool')
        diag.set_website('https://www.assembla.com/spaces/crisk')
        diag.set_license(crisk.__license__)
        x = diag.run()
        diag.hide()
        
    def on_open__activate(self, *args):
        filter = gtk.FileFilter()
        filter.add_pattern('*.crisk')
        selected_file = open_dialog('Open', filter = filter)
        if selected_file is None:
            return None
        try:
            db_url = 'sqlite:///%s' % selected_file
            metadata.bind = db_url
            metadata.bind.echo = True
            metadata.bind.has_table('model_asset')
            setup_all()
            self.db_file = selected_file
            self.tree.select(self.first)
            return True
        except Exception, info:
            error('Error opening database', str(info))
        
    def on_new__activate(self, *args):
        new_file = save('Save')        
        if new_file is None:
            return None

        if not new_file.endswith('.crisk'):
            new_file = new_file + '.crisk'
        
        try:
            db_url = 'sqlite:///%s' % new_file
            metadata.bind = db_url
            metadata.bind.echo = True
            setup_all()
            create_all()
            tmp = Basic()
            session.commit()
            self.db_file = new_file
            self.tree.select(self.first)
            return True
        except Exception, info:
            res = error("An error has ocurred", info.__str__())
            
    def on_exit__activate(self, *args):
        session.commit()
        gtk.main_quit()