#!/usr/bin/env python
# coding: utf-8 

import gtk
import pygtk
import sys, os

from model import *

from elixir import *
from os import path
from kiwi.ui.dialogs import error, warning, yesno, save, messagedialog
from kiwi.ui.dialogs import open as open_dialog
from kiwi.ui.objectlist import Column
from kiwi.ui.widgets import textview, label, entry
from kiwi.ui.delegates import GladeDelegate, GladeSlaveDelegate

class Step:
    def __init__(self, name, idx):
        self.name = name
        self.idx = idx

class BasicsView(GladeSlaveDelegate):
    def __init__(self):       
        GladeSlaveDelegate.__init__(self, 'ui', toplevel_name = 'BasicsWindow')
        widget_list = ['name', 'location', 'initial_date', 'scope']
        try:
            basics_model = Basic.get(1)
        except:
            print 'exception'
            basics_model = None
        print basics_model

        self.add_proxy(basics_model, widget_list)

class App(GladeDelegate):
    
    db_file = None

    def __init__(self):
       
        # Criando a tree inicial

        GladeDelegate.__init__(self, "ui", toplevel_name = 'MainWindow', 
                               delete_handler = gtk.main_quit)        
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
        results = tree.append(None, Step('Results', 4))
        tree.append(results, Step('Inventory Report', 5))
        tree.expand(results)
#        tree.select(self.first)

        if self.db_file is None:
            self.open_or_new()   
    
    def open_or_new(self):
        result = yesno('Choose \'Yes\' to open a previous work, or\n' + 
                       'choose \'No\' if you want to create a new DB') 
        if result == gtk.RESPONSE_YES:
            self.on_open__activate()
        elif result == gtk.RESPONSE_NO:
            self.on_new__activate()
        else:
            gtk.main_quit()
    
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
                        
    def on_about__activate(self, *args):
        diag = gtk.AboutDialog()
        x = diag.run()
        diag.hide()
               
    def on_open__activate(self, *args):
        filter = gtk.FileFilter()
        filter.add_pattern('*.crisk')
        selected_file = open_dialog('Open', filter = filter)
        if selected_file is None:
            return
        try:
            db_url = 'sqlite:///%s' % selected_file
            metadata.bind = db_url
            metadata.bind.has_table('model_asset')
            self.db_file = selected_file
            self.tree.select(self.first)
        except Exception, info:
            error('Error opening database', str(info))
        
    def on_new__activate(self, *args):
        new_file = save('Save')        
        if new_file is None:
            return
        
        if not new_file.endswith('.crisk'):
            new_file = new_file + '.crisk'
        
        try:
            db_url = 'sqlite:///%s' % new_file
            metadata.bind = db_url
            metadata.bind.echo = False
            setup_all()
            create_all()
            tmp = Basic()
            session.flush()
            self.db_file = new_file
            self.tree.select(self.first)
        except Exception, info:
            res = error("An error has ocurred", info.__str__())
            
        
app = App()
app.show_and_loop()