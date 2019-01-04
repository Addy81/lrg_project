
import os


def determine_if_show_ui(args):
	"""Determines whether the ui should be shown, based on the arguments
	provided. If the user has provided a file, lrgid or geneid argument flag
	to the program, the	UI is NOT shown, unless required for safety reasons
	(selecting the transcript or genome build when one has not been provided). 
	
	Args:
		args (dict): Dictionary containing command line arguments
	Returns:
		show_ui (bool): True or False whether the UI should be shown

	"""
	if (args['file'] == None and 
		args['lrgid'] == None and 
		args['geneid'] == None):
		show_ui = True
	else:
		show_ui = False
	return show_ui

def splashscreen():
	"""Displays the intial startscreen"""
	os.system('cls' if os.name == 'nt' else 'clear')
	print("="*40)
	print("")
	print("    LRG File Parsing Program")
	print("    Authors: A. Toutoudaki, J. Mahon")
	print("")
	print("="*40)

def ask_what_gene():
	"""Prompts the user to input a desired HGNC Gene Name

	Returns:
		selection (str): The gene name obtained from user input

	"""
	print("")
	print("    Please enter a HGNC Gene Name")
	print("")
	selection = input()
	return selection


def ask_which_genome_build(genomebuilds):
	"""Prompts the user to select the desired genome build. These are
	extracted from the XML file.

	Args:
		genomebuilds (list): List of different genome builds
	Returns:
		genome_choice (str): The genome build the user has selected
	
	"""
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
	genome_choice = genomebuilds[choice_int-1]
	return genome_choice


def ask_which_transcript(transcripts):
	"""Prompts the user to select the desired transcript. These are
	extracted from the XML file.

	Args:
		transcripts (list): List of different transcripts
	Returns:
		transcript_choice (str): The transcript the user has selected

	"""
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
	transcript_choice = transcripts[choice_int-1]
	return transcript_choice


def ask_include_introns():
	"""Asks the user whether they require introns in the BED file.

	Returns:
		choice (bool): True or False whether introns are to be included

	"""
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
	"""Asks the user whether they require introns in the BED file.
	
	Returns:
		choice (int): The size of the flanking region required

	"""
	print("")
	print("    What size of flanking region is required?")
	print("")
	print("    Enter a flanking length")
	print("       e.g 10 for a 10bp flank")
	print("       e.g 0 for no flanking region")
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