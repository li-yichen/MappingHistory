## python code
[1]scraper.py: scrapes JSAH journals.

[2]scraperfirstissuespatch.py: scrapes first issues of JSAH journals, which are somehow left out by first file.

[3]xmlwikifinder.py: scrapes output of wikifier in xml format, outputs json.

[4]xmlwikifinder_withgeo.py: same as above, with wikipedia coordinates added, also outputs json.

[5]us_location_address-01-24.py: cleans up locations and classifies work types from the SAHARA .csv file provided by SAHARA.
[5,previous version] us_location_address.py.

## libraries and prerequisites:
*libraries required for (3) and (4), which read wikifier output, are italicised.*

__*illinois wikifier*__ (3)(4)

download from: https://cogcomp.org/page/software_view/Wikifier

how to run: follow the readme in downloaded folder, and put all the article files in TextSample folder.

__requests__ (1)(2)
pip install requests

__*Beautiful Soup*__ (1)(2)(3)(4)
pip install beautifulsoup4

__*lxml*__ (3)(4)
pip install lxml

__*os*__ (1)(2)(3)(4)
came with python

__*strin*g__ (3)(4)
came with python

__*json*__ (3)(4)(5)
came with python

__*collections*__ (3)(4)
came with python

__csv__ (5)
came with python

## explanation of work types in us_location_address.py:

the worktypes dictionary, starting from line 20, could be edited to more fitting categories, please follow the format of:
'worktype':["example1","example2","example3",...],

## future work:
to topic model architectural materials, etc.

## team (students):
fall 2018: Sophia G., Yichen L., Nathan S., Junqing S.</br>
winter 2019: Junqing, Yichen.

## acknowledgements:
Dr. Dan Baciu, our instructor. Jon Jablonski, map librarian. Fabian Offert, part of WE1S team and instructor of ART185AI. Su Burtner, geography PhD student. Jackie Spafford, curator of Image Resource Center at Dept. of Art History. Mike Johnson, geography PhD student. The WE1S project. We also owe our knowledge from Rodger Luo, TA of MAT259A, who kindly helped explain the readme and package contents of Wikifier at the beginning.
