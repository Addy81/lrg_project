#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements
import xml.etree.ElementTree as ET 

xml_file = 'LRG_384.xml'

tree = ET.parse(xml_file)
root = tree.getroot()

LRG_code = xml_file.rstrip('.xml')

def get_exon_coords(root):
    ''' Pull LRG exon coordinates'''
    exon_coords = {}

    for exon in root.iter('exon'):
        if len(exon.attrib) == 1:
            for coord in exon.iter('coordinates'):
                coord_list = []
                if coord.attrib['coord_system'] == LRG_code:
                    coord_list.append(int(coord.attrib['start']))
                    coord_list.append(int(coord.attrib['end']))
                    exon_coords[exon.attrib['label']] = coord_list
                else:
                    pass
            
                
            

    for key in exon_coords.keys():
        print (key, exon_coords[key])

get_exon_coords(root)     
