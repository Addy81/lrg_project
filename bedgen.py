

import csv

def create_bed_contents(lrg_object, introns_choice):
	"""Creates the contents for the BED file. Returns a nested list with
	each row being [chromosome, start, end, label]
	
	Args:
		lrg_object (dict): An LRG_Object containing LRG ID, HGNC name etc
		introns_choice (bool): Include introns True or False
	Returns:
		bedcontents (list): Nested list of rows [chromosome, start, end, label]

	"""

	bedcontents = []
	
	# Adds exon rows
	for item in lrg_object.mapped_flanked_exon_coords:
		chromosome = "chr"+lrg_object.chromosome
		start = lrg_object.mapped_flanked_exon_coords[item][0]
		end = lrg_object.mapped_flanked_exon_coords[item][1]
		label = "Exon_"+str(item)
		if start > end:
			start, end = end, start
		else:
			pass
		bedcontents.append([chromosome, start, end, label])
	
	# Adds intron rows
	if introns_choice == True:
		for item in lrg_object.mapped_intron_coords:
			chromosome = "chr"+lrg_object.chromosome
			start = lrg_object.mapped_intron_coords[item][0]
			end = lrg_object.mapped_intron_coords[item][1]
			if start > end:
				start, end = end, start
			else:
				pass
			label = "Intron_"+str(item)
			bedcontents.append([chromosome, start, end, label])

	return bedcontents


def write_bed_file(filetowrite, bedheader, bedcontents):
	"""Writes the BED header and contents to file.

	Args:
		filetowrite (str): The filename to write to
		bedheader (list): The header to write. List of strings
		bedcontents (list): Nested list of rows [chromosome, start, end, label]
	Returns:
		Nothing
	Raises:
		SystemExit: If the file could not be written

	"""

	try:
		with open(filetowrite, 'w', newline='') as csv_file:
			writer = csv.writer(csv_file, delimiter="\t")
			writer.writerow(bedheader)
			for line in bedcontents:
				writer.writerow(line)
		print("")
		print("    BED file successfully written to " +  filetowrite)
		print("")
	except:
		print("    Could not write BED file. Check write permissions")
		raise SystemExit