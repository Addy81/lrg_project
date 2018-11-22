#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements
import xml.etree.ElementTree as ET
from collections import defaultdict
import re



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

exon_coords = defaultdict(list)
'''
for exon in root.iter('exon'):
    if len(exon.attrib) == 1:
        current_exon = exon.attrib['label']
        print (exon.attrib['label'])
        #print (exon, exon.attrib)
        for coord in exon.iter('coordinates'):
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
                exon_coords[exon.attrib['label']].append(coord_list)
            
for key in exon_coords.keys():
    print (key, exon_coords[key])
            
'''

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
    return exon_coords
    
#get_exon_coords(root)  

def get_real_exon_coords(NM_number):
    ''' Extract the exon coordinates that correspond to a specific transcript'''

    real_coordinates = {}

    for mapping in root.iter('mapping'):
        if NM_number == mapping.attrib['coord_system']:
            count = 0
            for item in mapping.iter('mapping_span'): 
                count +=1
                real_coords = []
                real_coords.append(int(item.attrib['other_start']))
                real_coords.append(int(item.attrib['other_end']))
                real_coordinates[count] = real_coords
        elif NM_number != mapping.attrib['coord_system']:
            print ('Sorry the transcript number you provided is invalid. Please try again')

            

    
    for key in real_coordinates.keys():
        print(key ,' : ',real_coordinates[key] )
        
def get_chr_coordinates(genome_ref):
    for mapping in root.iter('mapping'):
        if genome_ref in mapping.attrib['coord_system']:
            for mapping_span == mapping.iter('mapping_span'):
                print(mapping_span.attrib['lrg_start'],mapping_span.attrib['lrg_end'],mapping_span.attrib['other_start'],mapping_span.attrib['other_end'])


get_chr_coordinates('GRCh37')