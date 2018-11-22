#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements
import xml.etree.ElementTree as ET
from collections import defaultdict



"""
parser = argparse.ArgumentParser(description='Assimilate low res HLA type data.')
parser.add_argument('input', type = argparse.FileType(), help='input file .xlsx to be analysed')
parser.add_argument('output', help='output file file name to be generated')


#parser.add_argument('f', type=argparse.FileType('r'))
args = parser.parse_args()

input_file = '/mnt/storage/home/toutoua/projects/tt/NIHR_Assimilator/NIHR_Assimilator/user_uploads/wooey_files/a9/7a/a9d37b514c336c0f302cc740bd75bbb52f59cb7a/MAIN_DATA_copy.xlsx'

#print (input_file)

output_file = args.output
"""

xml_file = 'LRG_384.xml'

tree = ET.parse(xml_file)
root = tree.getroot()

LRG_code = xml_file.rstrip('.xml')

'''
for child in root:
    print (child.tag, child.attrib)


for x in root.iter('exon'):
    if len(x.attrib) == 1 :
        for key in x.attrib.keys():
            print (x.attrib[key])
        print (x.attrib)
 '''       

exon_coords = {}

for exon in root.iter('exon'):
    if len(exon.attrib) == 1:
        current_exon = exon.attrib['label']
        print (exon.attrib['label'])
        #print (exon, exon.attrib)
        for coord in root.iter('coordinates'):
            if exon.attrib['label'] == current_exon:
                coord_list = []
                if coord.attrib['coord_system'] == LRG_code:
                    coord_list.append('l')
                elif coord.attrib['coord_system'] == (LRG_code + 't1'):
                    coord_list.append('t')
                elif coord.attrib['coord_system'] == (LRG_code + 'p1'):
                    coord_list.append('p')
                else:
                    pass
            
                coord_list.append(int(coord.attrib['start']))
                coord_list.append(int(coord.attrib['end']))
                print (coord_list)
                exon_coords[exon.attrib['label']] = coord_list
            
#for key in exon_coords.keys():
#    print (key, exon_coords[key])
            

'''           
'coord_system': 'LRG_384',
 'start': '22976', 
 'end': '23159', 
 'strand': '1', 
 'mapped_from': 'GRCh38'}
'''