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
:mod:`crisk.vulnerabiliesview`
==============================

This module provides the Vulnerabilities slave view and list.
"""

import gtk
import gettext

from kiwi.ui.delegates import GladeDelegate, GladeSlaveDelegate, ProxyDelegate
from kiwi.ui.objectlist import ObjectList, Column
from kiwi.currency import currency
from kiwi.model import Model
from kiwi.ui.dialogs import yesno
from model import *
from elixir import *

_ = gettext.gettext

class VulnerabilitiesView(GladeSlaveDelegate):
    """
    Creates a new GladeSlaveView to be attached to the mainview.
    
    :param parent: The parent mainview to be used as parent for dialogs.
    :type parent: View
    """
    
    def __init__(self, parent):
        
        self.__parent = parent
        
        GladeSlaveDelegate.__init__(self,  
                                    gladefile = 'ui',
                                    toplevel_name = 'VulnerabilityWindow')
        
        self.list = self.get_widget('list_vulnerability')

        cols = [ Column('description', title = _('Description'), data_type = unicode,
                        expand = True, sorted = True, editable = True),
                 Column('severity', title = _('Severity'), data_type = int,
                        editable = True),
                 Column('chance', title = _('Probability'), data_type = int,
                        editable = True) ]
        
        self.list.set_columns(cols)
        
        vulns = Vulnerability.query().all()
        
        if vulns is not None:
            for item in vulns:
                self.list.append(item)
                
    def on_vuln_add__clicked(self, *args):
        
        new_vuln = Vulnerability(description = _('Enter description...'), chance = 0,
                                 severity = 0)
        self.list.append(new_vuln)
        
    def on_vuln_del__clicked(self, *args):
        selected = self.list.get_selected()
        self.list.remove(selected)
        selected.delete()
        session.commit()
        
    def on_list_vulnerability__cell_edited(self, *args):
        session.commit()