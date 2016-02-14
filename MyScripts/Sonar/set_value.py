#!/usr/bin/python
import sys
import xml.etree.ElementTree as ET
print "Processing file " + sys.argv[1]
tree = ET.parse(sys.argv[1])
root = tree.getroot()
copy = tree.getroot()
for element in root.findall('rule'):
    for checking in copy.findall('rule'):
        if (element.get('key') == checking.get('key')):
            root.remove(element)
for priority in root.iter('priority'):
	priority.text = str("BLOCKER")
tree.write('output.xml')
