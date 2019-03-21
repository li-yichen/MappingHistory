import pandas as pd
import json
import csv
import re
import string

US_States = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
	"Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
	"Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina",
	"North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
	"Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
US_States_Abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
work_type_dict = {
	'culture':["museum","Museum","theater","Theater","concert halls","Concert Halls","public art","Public art","galleries","Galleries","gallery","Galley","sculpture","Sculpture","monument","Monument","memorial","Memorial","mural","Mural","painting","Painting","art centers","Art centers"],
	'public services':["asylums","Asylums","hospitals","Hospitals","medical centers","Medical Centers","health facilities","Health Facilities","rehabilitation","Rehabilitation","clinics","Clinics","infrastructure","airport","Airport","Infrastructure","bridge","Bridge","dam","Dam","canal","Canal","highway","Highway","railroad","Railroad","wind turbines","Wind Turbines","freeways","transportation building","Transportation Building","Public works","Public Works","wharves","Wharves","wharf","Wharf","casinos","Casinos","civic","Civic","Post office","post office","Post Office","correctional institutions","prison","Prison","public building","Public Building","Public building","fire station","Fire Station","capitol","Capitol","courthouse","Courthouse","government","civic center","federal building","Federal Building","city hall","City Hall","town hall","Town Hall","post office","police stations","Police Stations"],
	'religion':["cathedral","Cathedral","chapel","Chapel","church","Church","convents","Convents","religious","Religious","monaster","places of worship","theological seminaries","Theological Seminaries","synagogue","temple","basilica","mosque","Mosque"],
	'education and research':["laboratories","Laboratories","research","Research","institute","Institute","education","Education","lecture halls","Lecture halls","libraries","library","school","School","Educational","educational","academic","university","University","universities","Universities","college","colleges"],
	'commerce and workspace':["office building","Office building","administrative building","Adaministrative building","pawnshops","Pawnshops","jewelers","Jewelers","car wash","Car wash","bank","Bank","commercial","Commercial","corporate headquarter","Corporate Headquarter","financial institution","inns","Inns","hotel","Hotel","motel","Motel","restaurant","Restaurant","shopping","Shopping","motion picture theater","store","Store","beauty shops","Beauty Shops","mercantile buildings","Mercantile Buildings","wholesalers","Wholesalers"],
	'residential':["apartments","Apartments","condominiums","Condominiums","dwelling","Dwelling","residence","Residence","residential","Residential","rental housing","Rental Housing","houses","Houses","public housing","Public Housing","Housing","housing","mansions","Mansions","agricultural","Agricultural","farms","Farms","flour mill","factories","Factories","industrial plants","Industrial Plants","smithies","Smithies","industrial buildings","Industrial Buildings"],
	
	#included in public services
	#'government':["civic","Civic","Post office","post office","Post Office","correctional institutions","prison","Prison","public building","Public Building","Public building","fire station","Fire Station","capitol","Capitol","courthouse","Courthouse","government","civic center","federal building","Federal Building","city hall","City Hall","town hall","Town Hall","post office","police stations","Police Stations"],
	#'infrastructure':["infrastructure","airport","Airport","Infrastructure","bridge","Bridge","dam","Dam","canal","Canal","highway","Highway","railroad","Railroad","wind turbines","Wind Turbines","freeways","transportation building","Transportation Building","Public works","Public Works","wharves","Wharves","wharf","Wharf","casinos","Casinos"],
	
	#theater included in culture
	#'recreational':["golf","Golf","theater","Theater","resort","Resort","theme park","Theme park","Theme Park","amusement park","Amusement Park","Amusement park","recreation","Recreation"],
	
	#included in edu and research
	#'research':["laboratories","Laboratories","research","Research","institute","Institute"],
	
	#included in commerce and workspace
	#'agricultural/industry':["agricultural","Agricultural","farms","Farms","flour mill","factories","Factories","industrial plants","Industrial Plants","smithies","Smithies","industrial buildings","Industrial Buildings"],
	#'funerary':["burial","Burial","cemeteries","Cemeteries","cemetry","Cemeteries","mausoleum","Mausoleum","graves","Graves","funerary buildings","Funerary Buildings","tomb","Tomb"],
	
	#not yet included
	#'healthcare':["asylums","Asylums","hospitals","Hospitals","medical centers","Medical Centers","health facilities","Health Facilities","rehabilitation","Rehabilitation"]
	# "national parks", "street furniture", "public parks", "office buildings", "bungalows", "theme parks","distilleries"
	}

material_type_dict = {
    'wood':['ash','beach','birch','cedar','cherry','deodar','fir','hemlock','hickory','log','mahogany',
            'maple','oak','palm','picket','pine','plank','sotol','teak','timber','walnut','wood'],
    #tin found in "tin roof"
    #picket
    'metal':['aluminum','brass','bronze','copper','gilding','gold','iron','lead','metal','nickel','onyx','steel','tin','titanium','zinc'],
    'stone':['alabaster','andesite','ashlar','basalt','boulder','breccia','coral stone','dolostone', 'gneiss','granite','gravel','kankar','laterite','lava rock','marble','moorum','oolit','pebble','quartzite','rhyolite','rock','schist',
    'shale','shingles','slate','stone','terrazzo','trap','travertine'],
    #building stones: http://www.gly.uga.edu/railsback/BS-Main.html
    'concrete':['concrete'],
    'glass':['glass','vitrolite'],
    'recycled':['found','machine','reuse','scavenge','telephone'],
    #something called "mixed media (machine parts)" and "decommissioned telephone switching devices"
    'earth':['adobe','bousillage','ceramic','clay','earth','mortar','mud','pise','terracotta','stucco'],
    #stucco, Mortar, 
    'others':['acrylic','brick','charcoal','fiberglass','grass','linen','meadow','mixed media','neon','nylon',
    		'plant','plastic','silk','shell','ribbon','water']    
}
#'pinwheel','flowers','plaster','boncoat','mosaic','oil','odified queen-post through truss','ood','paper','papier','pencil'

locations = pd.read_csv("/Volumes/MUNCH/ARTHI/f18_arthi_sahara/sahara-us-full-12-3.csv")
locations_dict = locations.to_dict(orient='records')

# below could be used if computer could process NLTK
# jar = '/Users/yichenli/Documents/GitHub/TERRI/stanford-ner-tagger/stanford-ner.jar'
# # model = '/Users/yichenli/Documents/GitHub/TERRI/stanford-ner-tagger/classifiers/english.all.3class.distsim.crf.ser.gz'
# model = '/Users/yichenli/Documents/GitHub/TERRI/edu/stanford/nlp/models/ner/english.all.3class.caseless.distsim.crf.ser.gz'
# # # Prepare NER tagger with english model
# ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

# def get_continuous_chunks(tagged_sent):
#     continuous_chunk = []
#     current_chunk = []

#     for token, tag in tagged_sent:
#         if tag != "O":
#             current_chunk.append((token, tag))
#         else:
#             if current_chunk: # if the current chunk is not empty
#                 continuous_chunk.append(current_chunk)
#                 current_chunk = []
#     # Flush the final current_chunk into the continuous_chunk, if any.
#     if current_chunk:
#         continuous_chunk.append(current_chunk)
#     return continuous_chunk


for location in locations_dict:
	location["city"] = ""
	location["county"] = ""
	location["parish"] = ""
	location["state"] = ""
	location["country"] = ""
	location["zipcode"] = ""
	location["date_early"] = ""
	location["Broad_Category"] = ""
	location["listofdates"] = []
	location['wood'] =location['metal'] = location['stone']=location['concrete']=location['glass']=location['recycled']=location['earth']=location['others']= False

	locationListOfWords = str(location["Location[6648]"]).split(". ")
	if len(locationListOfWords) == 4:
		if "Parish" in locationListOfWords[1]:
			#cases such as "Vacherie/St. James Parish. Louisiana. United States"
			#if address format is "city/ st. parish . state. country" (parish gets falsely segmented into 2 words)
			if "/" in locationListOfWords[0]:
				i = str(locationListOfWords[0]).index("/")
				location["city"] = str(locationListOfWords[0])[:i]
				location["parish"] = str(locationListOfWords[0])[(i+1):] + "." + str(locationListOfWords[1])
			else:
				#cases such as "St. James Parish. Louisiana. United States"
				location["parish"] = locationListOfWords[0] + "." + locationListOfWords[1]
		else:
			location["city"] = locationListOfWords[0]
			location["county"] = locationListOfWords[1]
		location["state"] = locationListOfWords[2]
		location["country"] = locationListOfWords[3]
	elif len (locationListOfWords) == 3:
		if locationListOfWords[1] in (US_States or US_States_Abbreviations):
			if "Parish" in locationListOfWords[0]:
				if "/" in locationListOfWords[0]:
					#cases such as "Melrose/Natchitoches Parish. Louisiana. United States"
					i = str(locationListOfWords[0]).index("/")
					location["city"] = str(locationListOfWords[0])[:i]
					location["parish"] = str(locationListOfWords[0])[(i+1):]
				else:
					# cases such as "Pointe Coupee Parish. Louisiana. United States"
					location["parish"] = locationListOfWords[0]
					location["state"] = locationListOfWords[1]
					location["country"] = locationListOfWords[2]
			elif "County" in locationListOfWords[0]:
				#cases such as "King William County. Virginia. United States"
				location["county"] = locationListOfWords[0]
 			else:
				location["city"] = locationListOfWords[0]
				location["county"] = ""
				location["state"] = locationListOfWords[1]
				location["country"] = locationListOfWords[2]
		elif locationListOfWords[2] in US_States or locationListOfWords[2] in US_States_Abbreviations:
			if "Parish" in locationListOfWords[1]:
				location["city"] = str(locationListOfWords[0])[:-3]
				location["county"] = ""
				location["parish"] = "St." + locationListOfWords[1]
				location["state"] = locationListOfWords[2]
				location["county"] =""
			else:
				location["city"] = locationListOfWords[0]
				location["county"] = locationListOfWords[1]
				location["state"] = locationListOfWords[2]
				location["country"] = ""
			if locationListOfWords[2] in US_States_Abbreviations:
				#normalize abbreviations to state full names
				i = US_States_Abbreviations.index(locationListOfWords[2])
				location["state"] = US_States[i]
	elif len(locationListOfWords) == 2:
		#cases such as "Bella Vista. Arkansas"
		location["city"] = locationListOfWords[0]
		location["state"] = locationListOfWords[1]
		if any(str.isdigit(c) for c in str(locationListOfWords[1])) == True:
			# checks for zip codes
			# I did not use "if locationListOfWords[1].isalpha() == False:" since
			# there could be with spaces in them
			# cases such as "Santa Barbara. CA 93106"
			location["zipcode"] = str(locationListOfWords[1])[-5:]
			state_abbrev = str(locationListOfWords[1]).replace(str(location["zipcode"]),"")[:2]
			i = US_States_Abbreviations.index(state_abbrev)
			location["state"] = US_States[i]
		elif str(locationListOfWords[1])[:2] in US_States_Abbreviations:
			#cases such as "Santa Barbara. CA"
			i = US_States_Abbreviations.index(str(locationListOfWords[1])[:2])
			location["state"] = US_States[i]
	if location["Date(s)[6620]"] is not None:
		sentence = str(location["Date(s)[6620]"])
		#if nltk is used
		# words = nltk.word_tokenize(sentence)
		# # Run NER tagger on words
		# ne_tagged_sent = ner_tagger.tag(words)
		# for a,b in ne_tagged_sent:
		# 	if b == 'DATE':
		# 		location["listofdates"].append(a)
		# 	else:
		# 		continue
		
		#creates a list of dates mentioned in each entry's "Date(s)[6620]" column, for storing all dates found in that column
		listofdates = []
		#finds dates in format of "200 to 127 BCE" or "635 BCE"
		dates_result_BCE = re.findall(r"(\d+)-(\d+) BCE",sentence) + re.findall(r"(\d+)BCE",sentence)
		#finds dates in format of "12th century" or "7th century"
		dates_result_Century = re.findall(r"(\d+)th",sentence)
		#finds dates in format of "1987-98"
		dates_result_range = re.findall("\d{4}"+"-"+"\d{2}",sentence)
		#finds dates in format of multiple digits, i.e. 103, 1926, etc.
		dates_result_rest = re.findall(r"\d+",sentence)
		
		#for dates with BCE years:
		if dates_result_BCE is not None:
			for date in dates_result_BCE:
				#in case of "200 to 127 BCE", which would lead to date in format of (200,127) tuple
				if type(date) is tuple:
					#converts each date to format of -200 and -127 (as numbers)
					for d in date:
						cd = int(d)
						cd = cd*(-1)
						listofdates.append(cd)
				#in case of "635 BCE", which would lead to date in format of 635 (as number)
				else:
					#converts date to format of -635 (as number)
					cd = int(date)
					cd = cd*(-1)
					listofdates.append(cd)
		#for dates with centuries:
		if dates_result_Century is not None:
			for date in dates_result_Century:
				#adds "00" after dates, for example, "19th" turns into "1900"
				cd = date+ "00"
				cd = int(cd)
				listofdates.append(cd)
		#for dates with ranges in format of "1987-98"
		if dates_result_range is not None:
			for date in dates_result_range:
				if len(str(date)) ==4:
					global dates_result_range_century
					dates_result_range_century = str(date[:2])
					cd = str(date[:2])
					listofdates.append(cd)
				if len(str(date)) == 2:
					cd = int(dates_result_range_century + str(date))
					listofdates.append(cd)
		#for dates in format of any consecutive multiple digits
		if dates_result_rest is not None:
			for date in dates_result_rest:
				if (date not in dates_result_BCE) and (date not in dates_result_Century) and (date not in dates_result_range):
					cd = int(date)
					if cd >100:
						listofdates.append(cd)
		location["listofdates"] = listofdates
		
		#finds earliest date mentioned out of list of dates
		if listofdates == []:
			location["date_early"] = "earliest date not found"
		else:
			location["date_early"] = min(listofdates)
				
	if location["parish"] is not "":
		#lists parish as county if parish exists
		location["county"] = location["parish"]
	listOfKeys = location.keys()

	for category, worktypes in work_type_dict.items():
		if any(word in str(location["Work Type[6647]"]) for word in worktypes):
			location["Broad_Category"] = category
		elif any(word in str(location["Keywords[6637]"]) for word in worktypes):
			location["Broad_Category"] = category
		elif any(word in str(location["Title/Name of Work[6617]"]) for word in worktypes):
			location["Broad_Category"] = category
		else:
			continue
	for material_types, materials in material_type_dict.items():
		if any(word in str(location["Materials/Techniques[6624]"]) for word in materials):
			i = material_types
			location[i] = True
		else:
			continue

csv_columns = listOfKeys
csv_file = "/Volumes/MUNCH/ARTHI/sahara-us-full-12-3.csv"
with open(csv_file, "w") as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
	writer.writeheader()
	for data in locations_dict:
		writer.writerow(data)

# j = json.dumps(locations_dict,indent=4)
# f =  open('/Volumes/MUNCH/ARTHI/sahara-us-full.json','w')
# print >> f, j
# f.close()