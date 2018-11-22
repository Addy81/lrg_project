#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements
import xml.etree.ElementTree as ET 


def get_exon_coords(root, lrg_id):
    ''' Pull LRG exon coordinates'''
    exon_coords = {}

    for exon in root.iter('exon'):
        if len(exon.attrib) == 1:
            for coord in exon.iter('coordinates'):
                coord_list = []
                if coord.attrib['coord_system'] == lrg_id:
                    coord_list.append(int(coord.attrib['start']))
                    coord_list.append(int(coord.attrib['end']))
                    exon_coords[exon.attrib['label']] = coord_list
                else:
                    pass
    return exon_coords
         

def get_real_exon_coords(root, NM_number):
    ''' Extract the exon coordinates that correspond to a specific transcript'''

    nm_exon_coordinates = {}
    for mapping in root.iter('mapping'):
        if NM_number == mapping.attrib['coord_system']:
            count = 0
            for item in mapping.iter('mapping_span'): 
                count +=1
                exon_coord_list = []
                exon_coord_list.append(int(item.attrib['other_start']))
                exon_coord_list.append(int(item.attrib['other_end']))
                nm_exon_coordinates[count] = exon_coord_list
        elif NM_number != mapping.attrib['coord_system']:
            pass
    return nm_exon_coordinates

