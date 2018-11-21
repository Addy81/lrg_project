#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements
import xml.etree.ElementTree as ET


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


tree = ET.parse('LRG_384.xml')

root = tree.getroot()

for child in root:
    print (child.tag, child.attrib)


for x in root.iter('exon'):
    if len(x.attrib) == 1 :
        for key in x.attrib.keys():
            print (x.attrib[key])
        print (x.attrib)
        

exons = {{}}

for exon in root.iter('exon'):
    if len(exon.attrib) == 1:
        for coord in root.iter('coordinates'):
            if coord.attrib == 'LRG_384':
