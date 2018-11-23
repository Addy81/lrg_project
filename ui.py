
import os

def splashscreen():
	os.system("clear")
	print("="*40)
	print("")
	print("    LRG Parsing Program")
	print("    Authors: A. Toutoudaki, J. Mahon")
	print("")
	print("="*40)


def ask_what_gene():
	print("")
	print("    Please enter a HGNC Gene ID")
	print("")
	selection = input()
	return selection


def ask_which_genome_build(genomebuilds):
	print("")
	print("    Which genome build would you like to use?")
	counter = 1
	for genomebuild in genomebuilds:
		print("    " + str(counter)+ " " + genomebuild)
		counter +=1		
	print("")
	validinput = False
	while validinput == False:
		choice = input()
		try:
			choice_int = int(choice)
			if choice_int >= 1 and choice_int <= len(genomebuilds):
				validinput = True
			else:
				print("Please enter a valid choice")
		except:
			print("Please enter a valid choice")
	print("")
	print("    Genome Build choice: " + genomebuilds[choice_int-1])
	print("")
	return genomebuilds[choice_int-1]


def ask_which_transcript(transcripts):
	print("")
	print("    Please select the desired transcript")
	counter = 1
	for transcript in transcripts:
		print("    " + str(counter)+ " " + transcript)
		counter +=1
	print("")
	validinput = False
	while validinput == False:
		choice = input()
		try:
			choice_int = int(choice)
			if choice_int >= 1 and choice_int <= len(transcripts):
				validinput = True
			else:
				print("Please enter a valid choice")
		except:
			print("Please enter a valid choice")

	print("")
	print("    Transcript choice: " + transcripts[choice_int-1])
	print("")
	return transcripts[choice_int-1]