

import csv

def create_bed_contents(lrg_object):
	bedcontents = []
	for item in lrg_object.nm_exon_coords:
		chromosome = "chr"+str(item)
		start = lrg_object.nm_exon_coords[item][0]
		end = lrg_object.nm_exon_coords[item][1]
		bedcontents.append([chromosome, start, end])
	return bedcontents


def write_bed_file(filetowrite, bedheader, bedcontents):
	try:
		with open(filetowrite, 'w', newline='') as csv_file:
			writer = csv.writer(csv_file, delimiter="\t")
			writer.writerow([bedheader, ""])
			for line in bedcontents:
				writer.writerow(line)
		print("")
		print("    BED file successfully written to " +  filetowrite)
		print("")
	except:
		print("    Could not write BED file. Check write permissions")