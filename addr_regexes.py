import re

addrRegex = re.compile(r"""^
((UNIT|APT?|SUITE|PH|TH|LPH|ROOM)\s?)?                             # 0-1 possible unit 
(\d+\s[A-D]|[A-Z]\s?\d+|\d+[A-Z]|\d+)                             # 2 number (mandatory)
\s                                                                # separator
(\d+\s[A-D]\s|\d+[A-Z]?\s|\d+\s)?                                 # 3 possible second number
(\d+\s[A-D]\s|\d+[A-Z]?\s|\d+\s)?                                 # 4 possible third number
([A-Z'\d\s]{2,}\s)?                                               # 5 street name
(RD|AVE|ST|BLVD|LNS?|DR|CT|CRES|GRV|HTS|PL|PT|GRN|HWY|CLOSE|
 CIR|TERR|NDR|LINE|PK|GATE|WALKWAY|WAY|GDNS?|TRAIL|MANOR|SHORES?|
 SQ|ESPL|COVE|PKWY|QUAY|PVT|MEWS|RIDGE|PLAZA|LANDNG|GLENWAY|GLEN|
 FALLS|DRIVEWAY|LANEWAY|ROSEWAY|WYND|CHASE|MOUNT|PROM|CONCESSION|
 BAY|SIDEROAD|CIRCT|BEND|LINK|VILLGE|ROUTE|HILLS?|VILLAS?|RISE|
 VIEW|ROW|CREEK|ESTATES?|HEATH|WALK|BEACH|ISLE|HARBR|ISLAND|
 PASS|KINGSWAY|PATH|WOODS?|ACRES|COMMON|HIGHROAD|DONWAY|INLET|
 FAIRWAYS?|QUEENSWAY|LOFT|MEADOWS?|COACHWAY|GOLFWAY|BLUFFS?|
 BERRYWAY|GRANDE|HOLLOW|KEEP|KNOLL|OUTLOOK|NEST|CROFT|
 COLLEGEWAY|HOMESTEAD|FOREST|ALLEY|VALLEYWAY|SHEPWAY|MILLWAY|
 GLADE|TLINE|GREENWAY|RIDGEWAY|RUN|PATHWAY|THICKET)               # 6 street suffix (mandatory)
(\s(NE|NW|SE|SW|N|E|S|W))?                                        # 7-8 possible street direction
(\s(UNIT|APT?|SUITE|PH|TH|LPH|ROOM)?\s?                                 
 ([A-Z]\s?\d+|\d+\s?[A-Z]|\d+|[A-Z]))?                            # 9-11 possible unit and number                                  
$""", re.VERBOSE)

ruralRegex = re.compile(r"""^   
(R\s?RD?\s?([A-Z\d]+)\s)?              # 0-1 rural route/range road
(LOT\s[A-Z\d]+\s)?                     # 2 lot
(SITE\s[A-Z\d]+\s)?                    # 3 site
(COMP\s[A-Z\d]+\s)?                    # 4 compartment
(R\s?RD?\s?([A-Z\d]+)\s?)?             # 5-6 rural route/range road 
(STN\s[A-Z\d\s]+\s?)??                 # 7 station (non-greedy)
(LCD\s[A-Z\d]+\s?)?                    # 8 letter carrier depot 
(RPO\s[A-Z\d]+\s?)?                    # 9 retail postal outlet 
(\d+\s)?                               # 10 first number
(\d+\s)?                               # 11 second number
((([A-Z'\d\s]{2,}\s)?
  (CONCESSION\sRD|CONCESSION|TWP\sRD|TWP|COUNTY\sRD|SIDE\sRD|SIDEROAD|HWY|ROUTE|SIDELINE|LINE|RD)\s\d+[A-Z]?)|
 (([A-Z'\d\s]{2,}\s)?(RD|CT|ST|CRES|LINE|LN|DR|PL|BAY|WAY|AVE|HWY|CONCESSION|TOWNSEND))|
 (BROADWAY|MAINWAY))?                  # 12-19 one of 3 types of roads
(\s(NE|NW|SE|SW|N|E|S|W))?             # 20-21 street direction 
(\s?R\s?RD?\s?([A-Z\d]+))?             # 22-23 rural route/range road
(\s(UNIT|APT?|SUITE)\s
 ([A-Z]\s?\d+|\d+\s?[A-Z]|\d+))?       # 24-26 possible unit and number         
$""", re.VERBOSE)

# for simplicity, only one-word street names are allowed for addresses with no street suffix
nosuffixRegex = re.compile(r"^(\d+[A-Z]?\s)(\d+\s)?([A-Z][A-Z'\d]+)(\s[NESW])?$")

# virtually identical to the addrRegex, except that there may be words before and after the core address
extrainfoRegex = re.compile(r"""^
(.+\s)??  # non-greedy
((UNIT|APT?|SUITE|PH|TH|LPH|ROOM)\s?)?                             
(\d+\s[A-D]\s|[A-D]\s?\d+\s|\d+[A-Z]\s|\d+\s)                                            
(\d+\s[A-D]\s|\d+[A-Z]?\s|\d+\s)?                     
(\d+\s[A-D]\s|\d+[A-Z]?\s|\d+\s)?                          
([A-Z][A-Z'\d\s]+\s)?  # street name should start with a letter                                      
(RD|AVE|ST|BLVD|LNS?|DR|CT|CRES|GRV|HTS|PL|PT|GRN|HWY|CLOSE|
 CIR|TERR|NDR|LINE|PK|GATE|WALKWAY|WAY|GDNS?|TRAIL|MANOR|SHORES?|
 SQ|ESPL|COVE|PKWY|QUAY|PVT|MEWS|RIDGE|PLAZA|LANDNG|GLENWAY|GLEN|      
 FALLS|DRIVEWAY|LANEWAY|ROSEWAY|WYND|CHASE|MOUNT|PROM|CONCESSION|
 BAY|SIDEROAD|CIRCT|BEND|LINK|VILLGE|ROUTE|HILL|VILLAS?|RISE|
 VIEW|ROW|CREEK|ESTATES?|HEATH|WALK|BEACH|ISLE|HARBR|ISLAND|
 PASS|KINGSWAY|PATH|WOODS?|ACRES|COMMON|HIGHROAD|DONWAY|INLET|
 FAIRWAYS?|QUEENSWAY|LOFT|MEADOWS?|COACHWAY|GOLFWAY|BLUFFS?
 BERRYWAY|GRANDE|HOLLOW|KEEP|KNOLL|OUTLOOK|NEST|CROFT|
 COLLEGEWAY|HOMESTEAD|FOREST|ALLEY|VALLEYWAY|SHEPWAY|MILLWAY|
 GLADE|TLINE|GREENWAY|RIDGEWAY|RUN|PATHWAY|THICKET)                                                          
(\s(NE|NW|SE|SW|N|E|S|W))?                                  
(\s(UNIT|APT?|SUITE|PH|TH|LPH|ROOM)?\s                                 
 ([A-Z]\s?\d+|\d+\s?[A-Z]|\d+|[A-Z]))?              
(\s.+)?                                  
$""", re.VERBOSE)

postalRegex = re.compile(r'^([A-Z][0-9]){3}$')

innernumRegex = re.compile(r'^\d+\s[A-Z]|\s\d+\s')

poboxRegex = re.compile(r'(P\s?O\s?)?BOX\s?(\d+),?')

floorRegex = re.compile(r'(\d+(ST|TH|ND|RD)\s(FLOOR|FLR?)),?|(FLOOR\s\d+),?')

streetnumRegex = re.compile(r'^(\d+|[A-Z]\d+|\d+[A-Z])$')
