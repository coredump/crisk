#!/usr/bin/env python

import gtk

from kiwi.ui.delegates import GladeDelegate, GladeSlaveDelegate, ProxyDelegate
from kiwi.ui.objectlist import ObjectList, Column
from kiwi.currency import currency
from kiwi.model import Model
from kiwi.ui.dialogs import yesno
from model import *
from elixir import *

class vuln:
    def __init__(self, name, state = False):
        self.description = name
        self.state = state

class TempModel(Model):
    def __init__(self, name = None, description = None, value = 0, vulns = None):
        self.invent_name = name
        self.invent_description = description
        self.invent_value = currency(value)
        self.vulns = vulns

class InventoryAddEdit(ProxyDelegate):
    def __init__(self, list_updater, edit = None):
        self.__edit = edit  
        self.__parent_populate_list = list_updater
        
        if edit is None:
            self.__tmp = TempModel()
        else:
            self.__tmp = TempModel(edit.name, edit.description, 
                                   edit.value, edit.vulns)
        
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
    
#    def proxy_updated(self, *args):
#        print args
#        
    def dialog_delete(self, *args):
        self.hide_and_quit()
    
    def on_invent_save_button__clicked(self, *args):
        model = self.__tmp
        if self.__edit is None:
            asset = Asset(name = model.invent_name,
                          description = model.invent_description,
                          value = model.invent_value)
        else:
            asset = self.__edit
            asset.name = model.invent_name
            asset.description = model.invent_description
            asset.value = model.invent_value
            
        session.commit()
        self.hide_and_quit()
        self.__parent_populate_list()
            
    def on_invent_cancel_button__clicked(self, *args):    
        self.hide_and_quit()

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
        self.populate_list()
        
    def populate_list(self):        
        try:
            invent_model = Asset.query().all()
        except:
            invent_model = None        

        if invent_model is not None:
            self.list.clear()
            for item in invent_model:
                self.list.append(item)
    
    def on_button_add__clicked(self, *args):
        add_view = InventoryAddEdit(list_updater = self.populate_list, edit = None)
        add_view.show(self.__parent)
        
    def on_button_del__clicked(self, *args):
        result = yesno('Really delete the selected asset?\n' + 
                       'This action can\'t be undone!')
        if result == gtk.RESPONSE_YES:
            selected = self.list.get_selected()
            selected.delete()
            session.commit()
            self.populate_list()
        else:
            pass
    
    def on_invent_list__row_activated(self, *args):
        self.on_button_edit__clicked()
    
    def on_button_edit__clicked(self, *args):
        selected = self.list.get_selected()
        if selected is not None:
            edit_view = InventoryAddEdit(list_updater = self.populate_list, 
                                         edit = selected)
            edit_view.show(self.__parent)