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

from geraldo import Report, landscape, ReportBand, TableBand, ObjectValue, \
                    Label, SystemField, BAND_WIDTH, FIELD_ACTION_SUM, \
                    FIELD_ACTION_COUNT
from geraldo.generators import PDFGenerator
from kiwi.currency import currency

from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

class BandFooter(ReportBand):
    height = 0.5*cm
    elements = [
    Label(text='Created by Crisk', top=0.1*cm, left=0),
            SystemField(expression='Page # %(page_number)d of %(page_count)d', top=0.1*cm,
            width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
    ]
    borders = {'top': True}

class BandHeader(ReportBand):
    height = 1.5*cm
    elements = [
                SystemField(expression='%(report_title)s', 
                            style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 16 }),
                Label(text = 'Asset', top = 1*cm, left = 0.5*cm,
                      style = {'fontName' : 'Helvetica-Bold'}),
                Label(text = 'Value', top = 1*cm, bottom = 0.3*cm, left = 13*cm,
                      style = {'fontName' : 'Helvetica-Bold'})
                ]
    borders = {'bottom' : True}

class BandSummary(ReportBand):
    height = 1*cm
    elements = [
                Label(text = 'Number of Assets:', top = 0.3*cm, left = 0.5*cm, 
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                ObjectValue(attribute_name = 'name', top = 0.3*cm, left = 5*cm, 
                      action = FIELD_ACTION_COUNT,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                Label(text = 'Total Value:', top = 0.3*cm, left = 10*cm, 
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),                      
                ObjectValue(attribute_name = 'value', top = 0.3*cm, left = 13*cm, 
                      action = FIELD_ACTION_SUM,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12})
                      #get_value = lambda val: currency(val.value).format(True, 2))
                ]
    borders = {'top' : True }

class BandBegin(ReportBand):
    height = 1*cm
    elements = [
                Label(text = "Inventory Report"),
                ]

class BandDetail(ReportBand):
    height = 0.6*cm
    elements = (
                ObjectValue(attribute_name='name', left = 0.5*cm, bottom = 0.1*cm,
                            top = 0.2*cm),
                ObjectValue(attribute_name='value', left = 13*cm, bottom = 0.1*cm, 
                            top = 0.2*cm,
                            get_value = lambda val: currency(val.value).format(True, 2))
                )
    #borders = {'all': True}


class InventoryReport(Report):
    title = 'Inventory Report'

    page_size = A4
    margin_left = 2*cm
    margin_top = 2*cm
    margin_right = 2*cm
    margin_bottom = 2*cm

    band_summary = BandSummary()
    band_page_header = BandHeader()
    #band_begin = BandBegin()
    band_detail = BandDetail()
    band_page_footer = BandFooter()
    