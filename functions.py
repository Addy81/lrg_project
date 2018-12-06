#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

#script to parse xml and pick out some elements
import xml.etree.ElementTree as ET 


def get_exon_coords(root, genome_choice, transcript_choice):
    '''Calculates genomic coordinates based on the mapping information for different reference genomes and transcripts. '''
    
    mapped_coordinates = {}
    
    #Iterates from the root of the xml tree to identify the mapping attributes
    for mapping in root.iter('mapping'):
        #Checks the reference genome requested by the user and extracts the correct mapping start and end coordinates
        if genome_choice == mapping.attrib['coord_system']:
            for mapping_span in mapping.iter('mapping_span'):
                mapped_start = int(mapping_span.attrib['other_start']) - 1
                mapped_end = int(mapping_span.attrib['other_end']) + 1
                strand = mapping_span.attrib['strand']

        #Checks the transcript requested by the user and calculates the genomic coordinates accordingly    
        if transcript_choice == mapping.attrib['coord_system']:
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
                # Coordinates are stored in a dictionary with exon numbers as keys and start stop coordinates as values i.e. {1: [23904870, 23904829]}
                mapped_coordinates[count] = coordinates
            
    return mapped_coordinates


def get_intron_coords(exon_coords):
    """ Calculate intron coordinates"""

    intron_coords = {}

    for key in exon_coords.keys():
        # Stopping at the last exon as if exon number is n, intron number will be n-1
        if (key+1) not in exon_coords.keys():
            break
        else:
            # checks if gene is in foward strand
            if (exon_coords[1][1] - exon_coords[1][0]) > 0:
                intron_start = exon_coords[key][1] + 1 
                intron_end = exon_coords[key+1][0] - 1
                intron_coords[key] = [intron_start, intron_end]
            # checks if gene is in reverse strand
            elif (exon_coords[1][1] - exon_coords[1][0]) < 0:
                intron_start = exon_coords[key][1] - 1 
                intron_end = exon_coords[key+1][0] + 1
                intron_coords[key] = [intron_start, intron_end]

    return intron_coords


def get_flanked_coords(exon_coords,flank=5):
    """ Provides adjuedted exon coordinates based on user input"""

    flanked_coords = {}

    for k,v in exon_coords.items():
        if (v[1]-v[0]) > 0:
            flanked_coords[k] = [(v[0] - flank), (v[1] + flank)]
        elif (v[1]-v[0]) < 0:
            flanked_coords[k] = [(v[0] + flank), (v[1] - flank)]

    return flanked_coords
