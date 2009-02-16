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

from tempfile import NamedTemporaryFile
from pylab import *
from elixir import *
from sqlalchemy import select, func

from crisk.model import *

general_colors = ( 'b', 'g', 'r', 'c', 'm', 'y', '#008B8B', '#B8860B', '#DAA520', 
                  '#4B0082', '#191970', '#FF4500', '#BC8F8F', '#CD853F')

def do_percent(part, total):
    tmp_percent = (float(part)/float(total)) * 100
    return round(tmp_percent)

class InventoryOwnerGraph:
    
    def do_assets_per_owner(self, owners):
        figure(1, figsize=(6,6), facecolor = 'w')
        #ax = axes([0.1, 0.1, 0.8, 0.8])
        total_assets = Asset.query().count()
        labels = []
        percents = []
        for item in owners:
            num_assets = len(item.assets)
            perc = do_percent(num_assets, total_assets)
            if perc < 1:
                continue
            labels.append(item.name)
            percents.append(perc)

        pie(percents, explode=None, labels=labels, autopct='%1.1f%%', 
            shadow=True, colors = general_colors)
        title('Number of assets per owner')

        tmp_file = NamedTemporaryFile()
#        tmp_file = open('temp.png', 'w+b')
        tmp_file.close()
        savefig(tmp_file.name, format = 'png', transparent = True)
        return tmp_file

    def do_value_per_owner(self, owners):
        fig = figure(facecolor = 'w')
        ax = fig.add_subplot(111)
        
        labels = []
        values = []
        for item in owners:
            val_assets = sum([x.value for x in item.assets])
            labels.append(item.name)
            values.append(val_assets)

        ind = range(len(labels))
        ax.bar(ind, values, 0.35, color = 'r')
        ax.set_title('Value of assets per owner')
        ax.set_xticklabels(labels, rotation = 'vertical')
    
if __name__ == '__main__':
    metadata.bind = 'sqlite:///x:/dev/Workspace/Crisk/src/teste.crisk'
    metadata.bind.echo = False
    setup_all()
    owners = Owner.query().all()
    g = InventoryOwnerGraph()
    g.do_value_per_owner(owners)