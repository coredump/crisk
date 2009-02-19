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

import gettext

from tempfile import NamedTemporaryFile
from pylab import *
from elixir import *
from sqlalchemy import select, func

from crisk.model import *

_ = gettext.gettext

general_colors = ( 'b', 'g', 'r', 'c', 'm', 'y', '#008B8B', '#B8860B', '#DAA520', 
                  '#4B0082', '#191970', '#FF4500', '#BC8F8F', '#CD853F')

def do_percent(part, total):
    tmp_percent = (float(part)/float(total)) * 100
    return round(tmp_percent)

class InventoryOwnerGraph:
    
    def do_assets_per_owner(self, owners):
        figure(dpi = 300, figsize=(6,6), facecolor = 'w')
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
        title(unicode(_('Number of assets per owner')))

        tmp_file = NamedTemporaryFile()
        tmp_file.close()
        savefig(tmp_file.name, format = 'png', transparent = True)
        return tmp_file

class VulnGraph:
    
    def do_total_vuln_graph(self, vulns):
        fig = figure(dpi = 300, figsize=(5,5), facecolor = 'w')
        axes = Axes(fig, [.2, .1, .7, .8])
        axes.autoscale_view()
        axes.set_autoscale_on(True)
        fig.add_axes(axes)
        x = [int(v.severity) for v in vulns]
        y = [int(v.chance) for v in vulns]
        s = []
        tmp = []
        dic = {}
        final_x = []
        final_y = []
        final_s = []
        for i in range(len(x)):
            tmp.append((x[i], y[i]))     
        for i in range(len(tmp)):
            if dic.has_key(tmp[i]):
                dic[tmp[i]] += 1
            else:
                dic.update({tmp[i] : 1})
        for j in dic.keys():
            final_x.append(j[0])
            final_y.append(j[1])
            final_s.append(dic[j])
        final_s = array(final_s)
        subplot(111)
        ax_max = 5.2
        ax_min = 0
        scatter(final_x, final_y, s = 150*final_s, c= 'r', marker = 'o', label = 'Risk', antialiased = True)
        axis([ax_min, ax_max, ax_min, ax_max])
        axvspan(0, 1, 0, 3/ax_max, facecolor = 'g', alpha = 0.2, lw = 0)
        axvspan(1, 2, 0, 2/ax_max, facecolor = 'g', alpha = 0.2, lw = 0)
        axvspan(2, 3, 0, 1/ax_max, facecolor = 'g', alpha = 0.2, lw = 0)

        axvspan(2, 5.2, 4/ax_max, 5.2/ax_max, facecolor = 'r', alpha = 0.2, lw = 0)
        axvspan(3, 5.2, 3/ax_max, 4/ax_max, facecolor = 'r', alpha = 0.2, lw = 0)
        axvspan(4, 5.2, 3/ax_max, 2/ax_max, facecolor = 'r', alpha = 0.2, lw = 0)
        title(_('Risk Matrix'))
        
        tmp_file = NamedTemporaryFile()
#        tmp_file = open('temp.png', 'w+b')
        tmp_file.close()
        savefig(tmp_file.name, format = 'png', transparent = True)
        return tmp_file
        
if __name__ == '__main__':
    #metadata.bind = 'sqlite:///x:/dev/Workspace/Crisk/src/teste.crisk'
    metadata.bind = 'sqlite:////home/coredump/workspace/Crisk/src/teste.crisk'
    metadata.bind.echo = False
    setup_all()
    owners = Owner.query().all()
    vulns = Vulnerability.query().all()
    g = VulnGraph()
    g.do_total_vuln_graph(vulns)