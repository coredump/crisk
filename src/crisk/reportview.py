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

from tempfile import TemporaryFile

from kiwi.ui.delegates import GladeSlaveDelegate

from model import *
from crisk.reports.invent_report import PDFGenerator
from crisk.reports.invent_report import InventoryReport


class ReportView(GladeSlaveDelegate):
    def __init__(self, parent, reptype = None):
    
            GladeSlaveDelegate.__init__(self, "ui", toplevel_name = 'ReportWindow')
            
            dic_reps = {'inventory' : self._inventory_report }
            
            print 'AAAAAAA', dic_reps
            self.show_report(report = dic_reps[reptype]())
    
    def show_report(self, report):
        print report
    
    def _inventory_report(self):
        
        temp = TemporaryFile()
        
        assets = Asset.query().all()
        report = InventoryReport(queryset = assets)
        report.generate_by(PDFGenerator, filename = temp)                         
        
        return temp