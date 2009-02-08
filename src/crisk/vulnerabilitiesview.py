#!/usr/bin/env python

import gtk

from kiwi.ui.delegates import GladeDelegate, GladeSlaveDelegate, ProxyDelegate
from kiwi.ui.objectlist import ObjectList, Column
from kiwi.currency import currency
from kiwi.model import Model
from kiwi.ui.dialogs import yesno
from model import *
from elixir import *


class VulnerabilitiesView(GladeSlaveDelegate):
    def __init__(self, parent):
        
        self.__parent = parent
        
        GladeSlaveDelegate.__init__(self,  
                                    gladefile = 'ui',
                                    toplevel_name = 'VulnerabilityWindow')
        
        self.list = self.get_widget('list_vulnerability')

        cols = [ Column('description', title = 'Description', data_type = unicode,
                        expand = True, sorted = True, editable = True),
                 Column('severity', title = 'Severity', data_type = int,
                        editable = True),
                 Column('chance', title = 'Probability', data_type = int,
                        editable = True) ]
        
        self.list.set_columns(cols)
        
        vulns = Vulnerability.query().all()
        
        if vulns is not None:
            for item in vulns:
                self.list.append(item)
                
    def on_vuln_add__clicked(self, *args):
        
        new_vuln = Vulnerability(description = 'Enter description...', chance = 0,
                                 severity = 0)
        self.list.append(new_vuln)
        
    def on_vuln_del__clicked(self, *args):
        selected = self.list.get_selected()
        self.list.remove(selected)
        selected.delete()
        session.commit()
        
    def on_list_vulnerability__cell_edited(self, *args):
        session.commit()