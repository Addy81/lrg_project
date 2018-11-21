#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements

import xml.etree.ElementTree as ET

tree = ET.parse('LRG_384.xml')

root = tree.getroot()

for child in root:
    print (child.tag, child.attrib)


for x in root.iter('exon'):
    if len(x.attrib) == 1 :
        for key in x.attrib.keys():
            print (x.attrib[key])
        print (x.attrib)
        

for x in root.iter('exon'):
    if len(x.attrib) == 2 :
        for key in x.attrib.keys():
            print (x.attrib[key])
        print (x.attrib)