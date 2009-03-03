#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 José de Paula Eufrásio Júnior

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
Simple tool that gets a csv correctly formated and translates into a XML file.
"""

import sys
import re

from xml.dom.minidom import Document

if len(sys.argv) > 2:
	csv = open(sys.argv[2])
	desired_group = sys.argv[1]
else:
	print >> sys.stderr, "Usage: %s desired_group file.csv" % sys.argv[0]
	sys.exit(1)

regex = r'^(.*?),(.*),(.*)$'
regex_c = re.compile(regex)

doc = Document()
master = doc.createElement('library')
doc.appendChild(master)
top_level = doc.createElement('group')
top_level.setAttribute('name', desired_group)
master.appendChild(top_level)

for line in csv.readlines():
	clean_line = line.replace('"','').strip()
	item, desc, long_desc = regex_c.match(clean_line).groups()	
	level = item.count('.')
	
	cont = doc.createElement('control')
	cont.setAttribute('level', str(level))
	cont.setAttribute('ref', item)
	cont_desc = doc.createElement('description')
	desc_text = doc.createTextNode(desc)
	cont_desc.appendChild(desc_text)
	cont_l_desc = doc.createElement('longdesc')
	cont.appendChild(cont_desc)
	if long_desc != '':
		l_desc_text = doc.createTextNode(long_desc)
		cont_l_desc.appendChild(l_desc_text)
	cont.appendChild(cont_l_desc)
	top_level.appendChild(cont)

print doc.toprettyxml(indent='  ')
