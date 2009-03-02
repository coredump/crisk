#!/usr/bin/env python
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

regex = r'^(.*?),(.*)$'
regex_c = re.compile(regex)

doc = Document()
master = doc.createElement('library')
doc.appendChild(master)
top_level = doc.createElement('group')
top_level.setAttribute('name', desired_group)
master.appendChild(top_level)

for line in csv.readlines():
	clean_line = line.replace('"','').strip()
	item, desc = regex_c.match(clean_line).groups()	
	level = item.count('.')

	cont = doc.createElement('control')
	cont.setAttribute('level', str(level))
	cont.setAttribute('id', item)
	cont_text = doc.createTextNode(desc)
	cont.appendChild(cont_text)
	top_level.appendChild(cont)

print doc.toprettyxml()
