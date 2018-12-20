# LRG Parsing Tool
Developed by Joseph Mahon and Adriana Toutoudaki during the Programming Week in November 2018 at the University of Manchester

### Contents

* [Project Brief](#project-brief)
	* [User Requirements](#user-requirements)
	* [Minimum Viable Product](#minimum-viable-product)
	* [Included Functionality](#included-functionality)
* [Planning &amp; Design](#planning--design)
	* [Software Safety](#software-safety)
	* [Flag / Flagless Mode](#flag--flagless-mode)
	* [External Packages and Dependencies](#external-packages-and-dependencies)
	* [Flowchart](#flowchart)
* [Testing](#testing)
* [Program Use](#program-use)

## Project Brief

### User Requirements
The user requirements were provided during the practical sessions, and were flexible, with the main aim to be able to parse LRG XML files, and extract exon locations from these. 

### Minimum Viable Product
- Parse LRG XML files
- Extract Exon locations

### Included Functionality
As the tool is being designed to be used in a clinical environment, extra functionality was included to improve ease of use, safety and tracability.
- Automatic download of LRG XML file when provided with a HGNC ID.
- Extraction of genome build and transcripts from LRG XML to ensure accurate mapping
- Fully labelled BED files and BED data rows for traceability and audit purposes.
- Use of flags to allow integration within a pipeline or automated workflow.
- User interface to allow simple use by staff with limited command line experience.
 


## Planning & Design
Ensuring that  software is developed according to best practice guidelines and testing is performed is essential when working in a clinical environment. Code that has not been written well, checked, reviewed and documented can pose a hazard to patient safety.

### Software Safety
It is essential when writing software in a clinical environment that any data used or created is recorded to provide a trackable audit trail. To ensure that this trail is made, all BED files created by this tool are saved with a filename that includes all appropriate information:
HGNC Gene ID, LRG ID, Genome Version, Transcript.  
This information is also included within the header of the LRG file to ensure that it is visible when loaded into a genome browser. Each row in the resulting BED file makes use of the [extended BED format](https://genome.ucsc.edu/FAQ/FAQformat.html) and includes the additional field ‘name’, which is used as a descriptor for the row.

### Flag / Flagless Mode
The tool has been written so that it can be run with a set of flags, which provide all of the information required to create a BED file. The minimum flags necessary for automated BED generation is one defining which LRG to use (by providing either an LRG ID, HGNC Gene Name, or LRG XML file), along with a transcript and genome assembly version. If one of these flags is missing, the user interface (UI) will display and prompt the user for their choice. Having this information is essential, as creating a BED file without defining a transcript is unsafe, especially in a clinical environment.

There are two other optional flags. These are not required for automated BED generation, and allow the user to specify whether they want to include intronic regions or add a flank to each region.

The program can also be run with no flags at all, which uses a terminal based UI to collect the information. If a user also provides flags which are incomplete, the UI will prompt the user for the missing items. The tool will not output a BED file unless the minimum safe information is provided. Flag use is detailed in [Program Use](#program-use) below.

### External Packages and Dependencies
When planning the development, multiple python packages were investigated to fulfill particular functions. For example, lxml is a package which builds upon the functionality offered by the etree.ElementTree package. It provides some enhanced functionality and a slightly simpler interface, but as it is not included in the python standard library it requires installation. This is generally straightforward, but compatibility issues can arise when using different operating systems, such as Windows, where lxml cannot be installed solely using `pip`.

As the xml processing performed by this tool is simple, it was determined that using etree.ElementTree was sufficient and the compatibility and external package management overhead required for lxml was unnecessary.

This choice does not mean that use of external packages should be discouraged, just that their use or non-use should be thoroughly investigated and justified.

### Modularity
The code has been separated into modules in distinct python files, each containing related functions (BED functions, UI functions, exon coordinate functions and web API functions. They are imported into the main LRG_parser.py file and functions within them are invoked by referencing `module.function_name()`.  This creates an uncluttered working environment, gives context to the use of particular functions, and modularity of code allows easy reuse in other projects.

### Flowchart
Below is a flowchart showing the operational flow of the program. It is expected that this can be used by future developers or maintainers.




## Testing
Insert stuff about why testing is important  
Unit testing, integration testing, functional testing  
Test coverage - coverage.py  

## Program Use
The program can be used with or without flag arguments.
### Without Flags
```python
python lrgparser.py
```
As no arguments have been provided, the program loads the UI and prompts the user for a gene, desired genome version\* and desired transcript\*.  
\**These are extracted from the LRG file which will be downloaded, no knowledge about available transcripts is required by the user.*

### With Flags
The program is flexible and can take multiple optional flags as arguments.

#### Main Arguments
Three flags are available to define the LRG to use. Only one of these should be provided:  

Short Flag | Long Flag | Description
 --- | --- | ---
`-f` | `--file`   | Takes an LRG XML file as an argument (e.g LRG_384.xml)
`-l` | `--lrgid`  | Takes an LRG ID as an argument (e.g LRG_384)
`-g` | `--gene`  | Takes an HGNC gene name as an argument (e.g MYH7)

#### Supplimentary Arguments
Additional flags can be used to indicate the desired reference genome version or desired transcript. If these are not given, the UI will ask the user for their preference. If these are provided along with one of the flags from above, BED file generation will be completely automated.

Short Flag | Long Flag | Description
 --- | --- | ---
`-t` | `--transcript` | Takes a transcript as an argument (e.g NM_000257.2)
`-r` | `--referencegenome` |  Takes a reference genome as an argument (e.g GRCh37.p13)

#### Other Arguments
These are other optional arguments which are not required for automated BED generation, but they provide functionality that may be useful.

Short Flag | Long Flag | Description
 --- | --- | ---
`-i` | `--introns` | If this flag is present, intronic regions will be included
`-fl` | `--flank` |  Takes a flank size in bases (Minimum 0, Maximum 5000)

### Examples
1. When you know the gene name, but not the LRG ID and you don't have a file  
   ```python lrgparser.py -g MYH7```  
   The UI will prompt for the user to choose a genome version and transcript.  

2. When you know the gene name, genome version and transcript you want  
   ```python lrgparser.py -g MYH7 -r GRCh37.p13 -t NM_000257.2```  
   As all necessary arguments for fully automated BED file generation have been provided. The UI will not run and the BED file is created with no user input  
3. When you have an LRG XML file, know the genome version but do not know which transcripts are available  
   ```python lrgparser.py -f LRG_384.xml -r GRCh37.p13```  
   The program will look at the XML file to find available transcripts and display the UI to prompt the user to choose one.  

4. When you know the gene name and transcript, and you want a flanking region of 200 bases on each region 
   ```python lrgparser.py -g MYH7 -t NM_000257.2 -fl 200```  
   The program will download the appropriate LRG XML file, parse it to find available genome versions and then display the UI to prompt the user to choose one.

 5. When you only know the LRG ID, but want the whole gene (both exonic and intronic regions)
   ```python lrgparser.py -l LRG_384 -i```  
   The program will download the appropriate LRG XML file, parse it to find available genome versions and transcripts. The UI will then prompt the user for their preference.

-----------------------------MISC------------------------------------

## Stuff chopped out of old readme.md, to shove back in somewhere
Project Elements:
- Inspect element from xml
- Identify exon locations
- Where are the introns?
- Identify differences in the transcript
- Return a BED

## Extra stuff to write about
Mention ISO/UKAS conformance
Not including information can have a negative effect  
Warning if not found  
Talk about code comments and docstrings  
Talk about documentation  
Talk about PEP8 and style guidelines  
Future maintenance  
Future direction - if had more time  
Seeking feedback - AT asked B7 for clarification about inclusion of introns. Mention importance of feedback in development of tools that are useful and safe. This is how agile development is performed  
Make log files?  
Include time and date?  
Broken HGNC name in filename and header, accidentally made into HGNCID, needs reverting  
ERROR HANDLING  
Check when strand is reversed - is it base inclusive? half or full indexed? 
Check whether because the exon start/stops are reversed so its small/big, that this doesnt mess up exon numbering - should they be reversed 40-1 instead of 1-40 in myh7?
windows compatibility - fwd/back slashes (eg in tests) - swap out?
If LRG_384 passed as arg, doesn;t ask for flanking region or whole introns
Change maximum flank size to greater than 5000?