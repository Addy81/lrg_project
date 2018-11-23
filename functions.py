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

def get_chr_coordinates(genome_ref,transcript):
    '''Calculates genomic coordinates based on the mapping information for different reference genomes and transcripts. '''
    
    mapped_coordinates = {}
    
    #Iterates from the root of the xml tree to identify the mapping attributes
    for mapping in root.iter('mapping'):
        #Checks the reference genome requested by the user and extracts the correct mapping start and end coordinates
        if genome_ref == mapping.attrib['coord_system']:
            for mapping_span in mapping.iter('mapping_span'):
                mapped_start = int(mapping_span.attrib['other_start']) - 1
                mapped_end = int(mapping_span.attrib['other_end']) + 1
                strand = mapping_span.attrib['strand']

        #Checks the transcript requested by the user and calculates the genomic coordinates accordingly    
        if transcript == mapping.attrib['coord_system']:
            count = 0
            
            for exon in mapping.iter('mapping_span'):
                count += 1
                coordinates = []

                # Option of whether the gene is on the forward or reverse strand
                if strand == '1':
                    exon_start = mapped_start + int(exon.attrib['lrg_start'])
                    exon_end = mapped_start + int(exon.attrib['lrg_end'])
                    coordinates.append(exon_start)
                    coordinates.append(exon_end)
                elif strand == '-1':
                    exon_start = mapped_end - int(exon.attrib['lrg_start'])
                    exon_end = mapped_end - int(exon.attrib['lrg_end'])
                    coordinates.append(exon_start)
                    coordinates.append(exon_end)

                #Coordinates are stored in a dictionary with exon numbers as keys and start stop coordinates as values i.e. {1: [23904870, 23904829]}
                mapped_coordinates[count] = coordinates
            
    return mapped_coordinates