
import os


def determine_if_show_ui(args):
	"""Determines whether the ui should be shown, based on the arguments
	provided. If the user has provided a file, lrgid or geneid argument flag
	to the program, the	UI is NOT shown, unless required for safety reasons
	(selecting the transcript or genome build when one has not been provided). 
	"""
	if (args['file'] == None and 
		args['lrgid'] == None and 
		args['geneid'] == None):
		show_ui = True
	else:
		show_ui = False
	return show_ui

def splashscreen():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("="*40)
	print("")
	print("    LRG File Parsing Program")
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


def ask_include_introns():
	print("")
	print("    Would you like to include whole introns?")
	print("")
	print("     Y/N")
	print("")
	validinput = False
	while validinput == False:
		choice = input()
		if choice == "Y" or choice == "y":
			choice = True
			validinput = True
		elif choice == "N" or choice == "n":
			choice = False
			validinput = True
		else:
			print("Please enter a valid choice")

	return choice


def ask_flank_size():
	print("")
	print("    Would you like to include flanking regions?")
	print("")
	print("    Enter a flanking length, e.g 10 for a 10bp flank")
	print("")
	validinput = False
	while validinput == False:
		choice = input()
		try:
			choice_int = int(choice)
			if choice_int >= 0:
				validinput = True
			else:
				print("Please enter a valid choice")
		except:
			print("Please enter a valid choice")

	return choice