# a module to help the my_unique.py file
from addr_regexes import *

street_abbr = {'ROAD':'RD', 'AVENUE':'AVE', 'AV':'AVE', 'STREET':'ST', 'BOULEVARD':'BLVD', 'LANE':'LN', 'DRIVE':'DR',
               'COURT':'CT', 'CRESCENT':'CRES', 'CRESC':'CRES', 'CR':'CRES', 'CRESENT':'CRES', 'GROVE':'GRV',
               'HEIGHTS':'HTS', 'PLACE':'PL', 'GREEN':'GRN', 'HIGHWAY':'HWY', 'CIRCLE':'CIR', 'CIRCL':'CIR',
               'TERRACE':'TERR', 'CRT':'CT', 'GARDENS':'GDNS', 'POINT':'PT', 'ESPLANADE':'ESPL', 'PARKWAY':'PKWY',
               'PRIVATE':'PVT', 'LANDING':'LANDNG', 'SQUARE':'SQ', 'PROMENADE':'PROM', 'CIRCUIT':'CIRCT',
               'VILLAGE':'VILLGE', 'RTE':'ROUTE', 'STR':'ST', 'WY':'WAY', 'PKY':'PKWY', 'PARK':'PK',
               'CONC':'CONCESSION', 'HARBOUR':'HARBR', 'HARBOR':'HARBR', 'PASSAGE':'PASS', 'LANES':'LNS',
               'TR':'TRAIL', 'GARDEN':'GDN', 'CRS':'CRES', 'CRESCEN':'CRES', 'ROUTE':'RTE', 'TOWNLINE':'TLINE',
               'DRVIE':'DR'}
# CONCESSION is not abbreviated so that "CONCESSION 6" doesn't become "CONC 6"
unabbr_street_names = ('CLOSE', 'LINE', 'GATE', 'WAY', 'TRAIL', 'MANOR', 'SHORE', 'SHORES', 'COVE', 'QUAY', 'MEWS',
                       'RIDGE', 'PLAZA', 'GLENWAY', 'FALLS', 'DRIVEWAY', 'LANEWAY', 'ROSEWAY', 'WYND', 'CHASE',
                       'MOUNT', 'BAY', 'SIDEROAD', 'BEND', 'LINK', 'ROUTE', 'HILL', 'HILLS', 'VILLA', 'VILLAS', 'RISE',
                       'VIEW', 'ROW', 'CREEK', 'ESTATE', 'ESTATES', 'HEATH', 'WALK', 'BEACH', 'ISLE', 'LANE',
                       'ISLAND', 'PASS', 'KINGSWAY', 'DONWAY', 'FAIRWAYS', 'PATH', 'WOODS', 'ACRES', 'COMMON',
                       'INLET', 'QUEENSWAY', 'LOFT', 'MEADOW', 'MEADOWS', 'COACHWAY', 'GOLFWAY', 'BLUFF', 'BLUFFS',
                       'BERRYWAY', 'GRANDE', 'HOLLOW', 'KEEP', 'KNOLL', 'OUTLOOK', 'NEST', 'CROFT', 'COLLEGEWAY',
                       'HOMESTEAD', 'FOREST', 'ALLEY', 'VALLEYWAY', 'SHEPWAY', 'MILLWAY', 'GLADE', 'GREENWAY',
                       'RIDGEWAY', 'RUN', 'PATHWAY', 'THICKET')
drxn_abbr = {'NORTH':'N', 'EAST':'E', 'SOUTH':'S', 'WEST':'W'}
drxns2 = {'N.E.':'NE', 'N.W.':'NW', 'S.E.':'SE', 'S.W.':'SW'}
rural_abbr = ((('RURAL ROUTE ', 'RURAL RTE '), 'RR '),
              (('RANGE ROAD ', 'RANGE RD ', 'RGE RD ', 'RGE ROAD '), 'RRD '),
              (('TOWNSHIP ROAD ', 'TOWNSHIP RD ', 'TWP ROAD '), 'TWP RD '))
unit_abbr = {'APARTMENT':'APT', 'TOWNHOUSE':'TH', 'STE':'SUITE'}
buildings = ('BUILDING', 'BLDG', 'CENTRE', 'CENTER', 'PLAZA', 'TOWER', 'PLACE', 'COURT')
careof_abbr = ('C/O', 'ATTN:', 'ATTN', 'A/C', 'A/S', 'ITF')
num_str = {'ONE':'1', 'TWO':'2'}

def get_int(s):
    """
    Returns the decimal digits of a string concatenated together.
    """
    return ''.join([c for c in list(s) if c.isdigit()])

def is_street_num(s):
    """
    Returns True if s is a "street number" (either a number or a number concatenated to a letter).
    """
    return streetnumRegex.search(s) is not None

def replace_suffix(lst):
    """
    Replaces a street suffix with its abbreviation.
    :param lst: list of words in an address
    :return: lst, with a street suffix potentially substituted
    """
    for i in range(len(lst)-1, -1, -1):
        for key in street_abbr:
            # if we've found a street suffix, we need to make sure it's not part of a street name (e.g. Avenue Road)
            if lst[i] == key:
                for j in range(i+1, len(lst)):
                    if lst[j] in street_abbr.values() or lst[j] in unabbr_street_names:
                        # if we've found another street suffix which comes after, return
                        return
                # otherwise, replace the suffix by its abbreviation
                lst[i] = street_abbr[key]
                return

def replace_stn(lst):
    """
    Replaces the word 'STATION' in an address with 'STN' if it's not part of a street name.
    :param lst: list of words in an address
    :return: lst, with 'STATION' potentially substituted
    """
    for i in range(len(lst)):
        if lst[i] == 'STATION':
            # if the word "station" is found, we need to make sure it's not part of a street name
            for j in range(i+1, len(lst)):
                # if one of the subsequent words is a street suffix, we need to make sure a street number
                # was present somewhere between the station and the suffix
                if lst[j] in street_abbr.values() or lst[j] in unabbr_street_names:
                    for k in range(i+1, j):
                        if lst[k].isdigit():
                            lst[i] = 'STN'
                            return
                    return  # otherwise, the word "station" was probably part of a street name
                # if we went all the way to the end, we've found the station name
                if j == len(lst)-1:
                    lst[i] = 'STN'
                    return

def replace_drxn(lst):
    """
    Replaces a direction (north, south, east, west) with its abbreviation in an address.
    :param lst: list of words in an address
    :return: lst, with a direction potentially substituted
    """
    for i in range(len(lst)-1, -1, -1):
        for key in drxn_abbr:
            if lst[i] == key:
                # if a direction word was found, we need to make sure it's not a street name, i.e.
                # the previous word isn't a street number and the next word isn't a street suffix
                if i < len(lst)-1 and lst[i+1] in street_abbr.values() and i > 0 and is_street_num(lst[i-1]):
                    return
                lst[i] = drxn_abbr[key]  # otherwise, replace the word with its abbreviation
                break

def replace_unit(lst):
    """
    Replaces a unit type (e.g. APARTMENT, TOWNHOUSE) with its abbreviation in an address.
    :param lst: list of words in an address
    :return: lst, with a unit type potentially substituted
    """
    for i in range(len(lst)-1):
        for key in unit_abbr:
            # if a unit word was found, the next word must be a street number
            if lst[i] == key and is_street_num(lst[i+1]):
                lst[i] = unit_abbr[key]
                return

def replace_rural(addr):
    """
    Replaces a rural road (e.g. 'RURAL ROUTE', 'RANGE ROAD', 'TOWNSHIP ROAD') with its abbreviation in an address.
    :param addr: list of words in an address
    :return: lst, with a rural road potentially substituted
    """
    for g in rural_abbr:
        for name in g[0]:
            if addr.startswith(name) or (' ' + name) in addr:  # so that "FORGE RD" isn't caught by "RGE RD'
                # replace the rural road words by their abbreviation
                addr = addr.replace(name, g[1])
                return addr
    return addr

def get_bldg(addr):
    """
    Removes and returns a building name from an address.
    :param addr: list of words in an address
    :return: building name
    """
    for bldg in buildings:
        for i in range(1, len(addr)):
            temp = addr[i].rstrip(',')
            # if a building word is found (e.g. BUILDING, TOWER):
            if temp == bldg:
                # if the word doesn't end with a comma and isn't the last word in the address and
                # (the next word ends with a comma or is the last word) and (the next word is a street
                # number or a letter)
                if (addr[i][-1] != ',' and i < len(addr)-1 and (addr[i+1][-1] == ',' or i == len(addr)-2)
                   and (len(addr[i+1]) == 1 and (addr[i+1].isalpha() or addr[i+1].isdigit()))):
                    temp = addr[i+1].rstrip(',')
                    building = addr[i] + ' ' + temp
                    del addr[i:i+2]  # delete the building name from the address
                    return building  # return the building name

                addr[i] = addr[i].rstrip(',')
                # we're going to look at all the words which come before the building word
                for j in range(i-1, -1, -1):
                    # if the word is a street number, we've gone too far - return
                    if is_street_num(addr[j]):
                        return ''
                    # if the word ends with a comma or is a street suffix,
                    # and it's not the previous word, it must be the building name
                    elif addr[j][-1] == ',' or addr[j] in street_abbr.keys() or addr[j] in street_abbr.values():
                        if j != i-1:
                            building = ' '.join(addr[j+1:i+1])
                            del addr[j+1:i+1]
                            return building
                        # if it was the previous word, then we weren't able to find the name; return
                        else:
                            return ''
                    # if we went all the way back to the first word, then we've found the building name
                    elif j == 0:
                        building = ' '.join(addr[:i+1])
                        del addr[:i+1]
                        return building
    return ''

def get_careof(addr):
    """
    Removes and returns the "care of" part of an address.
    :param addr: list of words in an address
    :return: "care of" part of the address
    """
    if len(addr) == 0:
        return ''
    # if the first word of the address is one of 'C/O', 'ATTN:', etc.:
    if addr[0] in careof_abbr:
        # we're going to look at all words which come after the first
        for i in range(1, len(addr)):
            if is_street_num(addr[i]):
                return ''
            # if the word ends with a comma, we've found the "care of" person
            elif addr[i][-1] == ',' or addr[i] in firm_abbr.values():
                careof = ' '.join(addr[1:i+1])[:-1]
                del addr[:i+1]  # delete the person from the address
                return careof   # return the name
            # if we went all the way to the end, we've found the "care of" person
            elif i == len(addr)-1:
                careof = ' '.join(addr[1:i+1])
                del addr[:]
                return careof
    return ''

def addr_processing(addr):
    """
    Standardizes an address field for further processing and removes the floor, PO box, buildling and 'care of' parts.
    :param addr: address
    :return: addr (cleaned), floor, pobox, bldg, careof
    """
    addr = addr.upper().strip()
    if len(addr) < 3:
        return addr, '', '', '', ''
    # replace direction abbreviations with periods (e.g. N.W.); need to do this before the periods are replaced
    for key in drxns2:
        if key in addr:
            addr = addr.replace(key, drxns2[key])
            break

    # replace the following characters with a space; commas dealt with later (so that identifying bldg is easier)
    for c in '.;:#()-\u2013\u2014':
        addr = addr.replace(c, ' ')
    addr = addr.replace(' ,', ',').replace(',', ', ').replace('\u2019', "'").replace('`', "'")
    addr = ' '.join(addr.split())
    # try to locate and extract the floor number and PO Box number, if they exist
    floor, pobox = '', ''
    mo = floorRegex.search(addr)
    if mo is not None:
        floor = get_int(mo.group(0))
        addr = addr.replace(mo.group(0), '')
    mo = poboxRegex.search(addr)
    if mo is not None:
        pobox = mo.group(2)
        addr = addr.replace(mo.group(0), '')

    # replace the rural words with abbreviations, e.g. Rural Route => RR
    addr = replace_rural(addr)

    addr = addr.split()
    # if the first word of the address is 'one' or 'two', replace them with their numeric equivalents
    if len(addr) > 0:
        for key in num_str:
            if addr[0] == key:
                addr[0] = num_str[key]
                break
    # try to locate and extract the building name, if present
    bldg = get_bldg(addr)
    if bldg != '':
        temp = get_bldg(addr)  # since there might be two names, e.g. Royal Bank Plaza, South Tower
        if temp != '':
            bldg += ' ' + temp
    # try to locate and extract the "care of" part, if present
    careof = get_careof(addr)

    if len(addr) == 0:  # if there's nothing left in the address, return what we have up to now
        return '', floor, pobox, bldg, careof
    # remove the commas
    addr = [word.rstrip(',') for word in addr]
    # replace the street suffix by its abbreviation
    replace_suffix(addr)
    # replace the word 'station' by 'stn' (for rural addresses)
    replace_stn(addr)
    # replace the direction by its abbreviation
    replace_drxn(addr)
    # replace the unit word (e.g. 'apartment') by its abbreviation
    replace_unit(addr)
    # join the words in the address back together
    addr = ' '.join(addr).strip()
    return addr, floor, pobox, bldg, careof
