#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Module containing exon/intron extraction and calculation functions."""


import xml.etree.ElementTree as ET 


def get_exon_coords(root, genome_choice, transcript_choice):
    """Calculates the genomic coordinates of each exon. It uses the mapping
    information in the XML and the genome build and transcript provided by 
    the user.
    """
    mapped_coordinates = {}
    
    # Iterates from the root of the xml tree to identify mapping attributes.
    for mapping in root.iter('mapping'):
        # Checks the reference genome requested by the user and extracts the
        # correct mapping start and end coordinates.
        
        if genome_choice == mapping.attrib['coord_system']:
            for mapping_span in mapping.iter('mapping_span'):
                mapped_start = int(mapping_span.attrib['other_start']) - 1
                mapped_end = int(mapping_span.attrib['other_end']) + 1
                strand = mapping_span.attrib['strand']


        # Checks the transcript requested by the user and calculates the 
        # genomic coordinates accordingly.
        if transcript_choice == mapping.attrib['coord_system']:
            count = 0
            
            for exon in mapping.iter('mapping_span'):
                count += 1
                coordinates = []

                # Mapping differs depending on whether the gene is on the 
                # forward or reverse strand
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
                # Coordinates are stored in a dictionary with exon numbers as 
                # keys, with start and stop coordinates as values 
                # i.e. {'1': [23904870, 23904829]}
                mapped_coordinates[count] = coordinates
            
    print(len(mapped_coordinates))

    return mapped_coordinates


def get_intron_coords(exon_coords):
    """Calculates the genomic coordinates of each intron. It uses the already
    mapped exon coordinates, and maps an intron as the gap between each exon.
    Introns coordinates do not include flanking regions.
    """
    intron_coords = {}

    for key in exon_coords.keys():
        # Stop at the last exon as total exons = n, total introns = n-1
        if (key+1) not in exon_coords.keys():
            break
        else:
            # Check if the gene is on the foward strand
            if (exon_coords[1][1] - exon_coords[1][0]) > 0:
                intron_start = exon_coords[key][1] + 1 
                intron_end = exon_coords[key+1][0] - 1
                intron_coords[key] = [intron_start, intron_end]
            # Check if the gene is on the reverse strand
            elif (exon_coords[1][1] - exon_coords[1][0]) < 0:
                intron_start = exon_coords[key][1] - 1 
                intron_end = exon_coords[key+1][0] + 1
                intron_coords[key] = [intron_start, intron_end]

    return intron_coords


def get_flanked_coords(exon_coords,flank=0):
    """Adjusts the flanking regions for each exon based on user input."""

    flanked_coords = {}

    for k,v in exon_coords.items():
        if (v[1]-v[0]) > 0:
            flanked_coords[k] = [(v[0] - flank), (v[1] + flank)]
        elif (v[1]-v[0]) < 0:
            flanked_coords[k] = [(v[0] + flank), (v[1] - flank)]

    return flanked_coords
