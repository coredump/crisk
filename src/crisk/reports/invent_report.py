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

from geraldo import Report, landscape, ReportBand, ObjectValue
from geraldo.generators import PDFGenerator
from crisk.model import *

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

class InventoryReportBand(ReportBand):
    height = 0.5*cm
    elements = (
                ObjectValue(attribute_name='name', left = 0.5*cm),
                ObjectValue(attribute_name='value', left = 3*cm)
                )

class InventoryReport(Report):
    title = 'Inventory Report'
    author = 'Blergh'

    page_size = landscape(A4)
    margin_left = 2*cm
    margin_top = 0.5*cm
    margin_right = 0.5*cm
    margin_bottom = 0.5*cm

    band_detail = InventoryReportBand()