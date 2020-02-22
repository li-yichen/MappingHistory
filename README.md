## python code
[1]scraper.py: scrapes JSAH journals.</br></br>
[2]scraperfirstissuespatch.py: scrapes first issues of JSAH journals, which are somehow left out by first file.</br></br>
[3]xmlwikifinder.py: scrapes output of wikifier in xml format, outputs json.</br></br>
[4]xmlwikifinder_withgeo.py: same as above, with wikipedia coordinates added, also outputs json.</br></br>
[5]us_location_address-01-24.py: cleans up locations and classifies work types from the SAHARA .csv file provided by SAHARA.</br></br>
[5,previous version] us_location_address.py.</br></br>

## libraries and prerequisites:
*libraries required for (3) and (4), which read wikifier output, are italicised.*</br></br>
__*illinois wikifier*__ (3)(4)</br>
download from: https://cogcomp.org/page/software_view/Wikifier</br>
how to run: follow the readme in downloaded folder, and put all the article files in TextSample folder.</br>

__requests__ (1)(2)</br>
pip install requests</br>

__*Beautiful Soup*__ (1)(2)(3)(4)</br>
pip install beautifulsoup4</br>

__*lxml*__ (3)(4)</br>
pip install lxml</br>

__*os*__ (1)(2)(3)(4)</br>
came with python</br>

__*strin*g__ (3)(4)</br>
came with python</br>

__*json*__ (3)(4)(5)</br>
came with python</br>

__*collections*__ (3)(4)</br>
came with python</br>

__csv__ (5)</br>
came with python</br>
## explanation of work types in us_location_address.py:
the worktypes dictionary, starting from line 20, could be edited to more fitting categories, please follow the format of:
'worktype':["example1","example2","example3",...],</br>
## future work:
to topic model architectural materials, etc.</br>
## team (instructor):
Dr. Dan Baciu
## team (students):
fall 2018: Sophia G., Yichen L., Nathan S., Junqing S. | seminar project of mapping the image collection of the SAH, with ArcGIS and sort-of processed data. </br>
winter 2019: Junqing, Yichen. | started mapping the journal papers too </br>
spring 2019: Junqing, Yichen, Cindy Kang(MS student at MAT). | mapping the journal papers with tools other than ArcGIS</br>
after spring 2019: Yichen is not part of team
## acknowledgements:
Dr. Dan Baciu, our instructor. Jon Jablonski, map librarian. Fabian Offert, part of WE1S team and instructor of ART185AI. Su Burtner, geography PhD student. Jackie Spafford, curator of Image Resource Center at Dept. of Art History. Mike Johnson, geography PhD student. The WE1S project. We also owe our knowledge from Rodger Luo, TA of MAT259A, who kindly helped explain the readme and package contents of Wikifier at the beginning.
