#!/usr/bin/env python

import gtk

from kiwi.ui.delegates import GladeDelegate, GladeSlaveDelegate, ProxyDelegate
from kiwi.ui.objectlist import ObjectList, Column
from kiwi.currency import currency
from kiwi.model import Model
from model import *
from elixir import *

class vuln:
    def __init__(self, name, state = False):
        self.description = name
        self.state = state

class TempModel(Model):
    def __init__(self, name = None, description = None, value = None, vulns = None):
        self.invent_name = name
        self.invent_description = description
        self.invent_value = value
        self.vulns = vulns
        

class InventoryAddEdit(ProxyDelegate):
    
    def __init__(self, edit = False):
        self.__edit = edit  
        self.__tmp = TempModel()
        print 'tmp 1', self.__tmp
        proxy_widgets = ['invent_name', 'invent_value', 'invent_description']
        ProxyDelegate.__init__(self, self.__tmp, proxy_widgets, 'ui', 
                               toplevel_name = 'InventoryAddWindow', 
                               delete_handler = self.dialog_delete)  

        # Arvore de vulnerabilidades
        
        cols = [ Column('description', title = 'Description', data_type = unicode, 
                        expand = True),
                 Column('state', title = 'Applicable?', data_type = bool, 
                        editable = True)]
        
        self.tree = self.get_widget('invent_vuln_list')
        self.tree.set_columns(cols)
        
        all_vulns = Vulnerability.query().all()
        
        if self.__edit:
            pass
        else:
            for item in all_vulns:
                vuln_to_add = vuln(item.description)
                self.tree.append(vuln_to_add)
    
    def proxy_updated(self, *args):
        print args
        
    def dialog_delete(self, *args):
        pass
    
    def on_invent_save_button__clicked(self, *args):
#        list = self.tree.get_data()
#        print list
    

        model = self.__tmp
        print 'Self.model:', model
        asset = Asset(name = model.invent_name,
                      description = model.invent_description,
                      value = model.invent_value)
        session.commit()
        self.hide_and_quit()
            
    
    def on_invent_cancel_button__clicked(self, *args):    
        pass

class InventoryView(GladeSlaveDelegate):
    def __init__(self, parent):
        
        self.__parent = parent
        
        GladeSlaveDelegate.__init__(self,  
                                    gladefile = 'ui',
                                    toplevel_name = 'InventoryWindow')

        self.list = self.get_widget('invent_list')
        
        cols = [ Column('name', title = 'Name', data_type = unicode, 
                        searchable = True, sorted = True),
                 Column('description', title = 'Description', data_type = unicode, 
                        expand = True),
                 Column('value', title = 'Value', data_type = currency)]
        
        self.list.set_columns(cols)
        
        try:
            invent_model = Asset.query().all()
        except:
            invent_model = None        

        if invent_model is not None:
            for item in invent_model:
                self.list.append(item)
    
    def on_cell_edited(self, *args):
        print args
    
    def on_button_add__clicked(self, *args):
        add_view = InventoryAddEdit()
        add_view.show(self.__parent)
        
    def on_button_del__clicked(self, *args):
        print 'del'
