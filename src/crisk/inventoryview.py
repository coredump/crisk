#!/usr/bin/env python

from kiwi.ui.delegates import GladeSlaveDelegate
from kiwi.ui.objectlist import ObjectList, Column
from kiwi.currency import currency
from model import *
from elixir import *

class InventoryView(GladeSlaveDelegate):
    def __init__(self):
        
        GladeSlaveDelegate.__init__(self,  
                                    gladefile = 'ui',
                                    toplevel_name = 'InventoryWindow')

        self.list = self.get_widget('invent_list')
        
        cols = [ Column('name', title = 'Name', data_type = unicode, 
                        searchable = True, editable = True, sorted = True),
                 Column('description', title = 'Description', data_type = unicode, 
                        editable = True, expand = True),
                 Column('value', title = 'Value', data_type = currency, editable = True)]
        
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
        new_asset = Asset()
        item = self.list.append(new_asset, select = True)
        
    def on_button_del__clicked(self, *args):
        print 'del'