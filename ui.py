
import os

def splashscreen(xml_file):
	os.system("clear")
	print("="*40)
	print("")
	print("    LRG Parsing Program")
	print("    Authors: A. Toutoudaki, J. Mahon")
	print("")
	print("="*40)
	print("")
	print("    Parsing LRG XML File: " + xml_file)
	print("")
	print("="*40)

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
			if choice_int >= 1 and choice_int <= len(transcripts)+1:

				validinput = True
			else:
				pass
		except:
			print("Please enter a valid choice")

	return transcripts[choice_int-1]