from addr_regexes import *
from addr_processing import addr_processing

def get_rural_addr(s):
    """
    Breaks down a cleaned address field into rural components.
    :param s: cleaned address field (returned from addr_processing)
    :return: [unit_type, unit, street_num, street_name, suffix, drxn, rr, lot, site, comp, stn, lcd, rpo], rural_flag
    """
    mo = ruralRegex.search(s)
    if mo is None:
        return False  # return False instead of a list of empty strings so that the next regex will be attempted
    g = list(mo.groups())

    repeats = (0, 5, 22)  # the group positions for RR
    rr = ''
    for i in repeats:  # shouldn't have more than one RR
        if g[i] is not None:
            if rr != '':
                return ['']*13  # return a list of empty strings so that the next regex will NOT be attempted
            rr = g[i+1]
    if g[12] is not None and innernumRegex.search(g[12]) is not None:
        return False  # street name shouldn't have an inner number; try the next regex

    lot, site, comp, stn, lcd, rpo, unit_type, unit, street_num, street_name, suffix, drxn = ['']*12
    if g[2] is not None:
        lot = g[2][4:-1]
    if g[3] is not None:
        site = g[3][5:-1]
    if g[4] is not None:
        comp = g[4][5:-1]
    if g[7] is not None:
        stn = g[7][4:].rstrip()
    if g[8] is not None:
        lcd = g[8][4:].rstrip()
    if g[9] is not None:
        rpo = g[9][4:].rstrip()
    if g[21] is not None:
        drxn = g[21]

    if g[13] is not None:
        # e.g. 1024 DRUMMOND CONCESSION RD
        street_name = g[13]
    elif g[17] is not None:
         # e.g. 1024 9TH LINE
        street_name = g[17].rstrip()
    elif g[19] is not None:
        # e.g. 1024 BROADWAY
        street_name = g[19]
    if g[18] is not None:
        suffix = g[18]
        if g[11] is not None and g[17] is None:
            # e.g. 1024 5 AVE
            street_name = g[11][:-1]

    if g[10] is not None:
        if g[11] is not None:  # 2 numbers were present
            if street_name != '':
                # if there was a street name, the first number was a unit number
                unit = g[10][:-1]
                street_num = g[11][:-1]
            else:
                # if there was no street name, the second number was the street name
                street_num = g[10][:-1]
        else:
            street_num = g[10][:-1]

    if unit != '' and g[26] is not None:
        return False  # can't have two units
    elif unit == '' and g[26] is not None:
        unit_type = g[25]
        unit = g[26]
    if street_name != '' and street_num == '':
        return False  # can't have a street name with no street number

    if rr == '' and street_name == '' and stn == '':
        return False  # at least one of these should be present
    return [unit_type, unit, street_num, street_name, suffix, drxn, rr, lot, site, comp, stn, lcd, rpo]

def get_addr(s):
    """
    Breaks down a cleaned [urban] address into its component parts.
    :param s: cleaned address field (returned from addr_processing)
    :return: [unit_type, unit, street_num, street_name, suffix, drxn, '', '', '', '', '', '', '']
    """
    mo = addrRegex.search(s)
    if mo is None:
        return False  # try the next regex
    g = list(mo.groups())
    # if a rural road was found in the address, send it to get_rural_addr instead
    if g[10] is None and g[11] is not None and g[6] in ('RD', 'HWY', 'LINE', 'ROUTE', 'SIDELINE', 'SIDEROAD'):
        # no unit type and a number at the end of the address, e.g. HWY 7
        return False

    if g[5] is not None:
        g[5] = g[5][:-1]  # strip space on the right
        # if the street name starts with one letter and then a space, and that letter wasn't a direction:
        if len(g[5]) > 2 and g[5][1].isspace() and g[5][0].isalpha() and g[5][0] not in 'NESW':
            # if the street number ends with a space and a letter, we probably grouped it wrong;
            # that letter likely belongs to the street name (e.g. "1 C K S O RD")
            if g[3] is None and len(g[2]) > 2 and g[2][-1].isalpha() and g[2][-2].isspace():
                g[5] = g[2][-1] + ' ' + g[5]  # add the letter to the street name
                g[2] = g[2][:-2]              # remove the letter from the street number
            # likewise for if the street number was in group 3
            elif g[3] is not None and g[4] is None:
                g[3] = g[3].rstrip()
                if len(g[3]) > 2 and g[3][-1].isalpha() and g[3][-2].isspace():
                    g[5] = g[3][-1] + ' ' + g[5]
                    g[3] = g[3][:-2]

    # remove spaces and leading 0s from the number parts
    g[2] = g[2].replace(' ', '').lstrip('0')
    if g[11] is not None:
        g[11] = g[11].replace(' ', '').lstrip('0')
    if g[3] is not None:
        g[3] = g[3].replace(' ', '')
    if g[4] is not None:
        g[4] = g[4].replace(' ', '')

    unit_type, unit, street_num, street_name, drxn = ['']*5
    suffix = g[6]
    if g[5] is not None and innernumRegex.search(g[5]) is not None:
        return False  # street name shouldn't have an inner number
    if g[8] is not None:
        drxn = g[8]
    if g[0] is not None:
        if g[11] is not None or g[3] is None:
            return ['']*13  # can't have two unit numbers; can't only have a unit number
        unit_type = g[1]
        unit = g[2]
    elif g[11] is not None:
        if g[4] is not None or (g[3] is not None and g[5] is not None):
            return ['']*13  # can't have two unit numbers
        if g[10] is not None:
            unit_type = g[10]
        unit = g[11]
    if g[3] is not None and g[4] is not None and g[5] is not None:
        return ['']*13  # can't have three numbers and then a street name

    if g[3] is None and g[4] is None and g[5] is not None:
    # e.g. 80 STREET_NAME DR
        street_num = g[2]
        street_name = g[5]
    elif g[3] is not None and g[4] is None and g[5] is not None:
    # e.g. 2007 97 STREET_NAME ST
        unit = g[2]
        street_num = g[3]
        street_name = g[5]
    elif g[3] is not None and g[4] is None and g[5] is None:
    # e.g. 612 5 AVE
        street_num = g[2]
        street_name = g[3]
    elif g[3] is not None and g[4] is not None and g[5] is None:
    # e.g. 6 1200 75 AVE
        unit = g[2]
        street_num = g[3]
        street_name = g[4]
    else:
        return False  # if it doesn't follow any of the rules above
    return [unit_type, unit, street_num, street_name, suffix, drxn, '', '', '', '', '', '', '']

def get_extrainfo_addr(s):
    """
    Breaks down a cleaned [urban] address with extra information in it into its component parts.
    :param s: cleaned address field (returned from addr_processing)
    :return: address components (sent to get_addr), addr_rest
    """
    mo = extrainfoRegex.search(s)
    if mo is None:
        return False, ''

    # create a new address which will be passed to get_addr
    new = ''.join([x for x in [mo.group(i) for i in (2, 4, 5, 6, 7, 8, 9, 11)] if x is not None])
    addr_rest = [x.strip() for x in [mo.group(1), mo.group(14)] if x is not None]
    # the keywords below are not allowed to be in addr_rest (otherwise we're probably parsing the address incorrectly)
    keywords = ('RR', 'RRD', 'CONCESSION', 'HWY', 'ROUTE')
    for word in addr_rest:
        if word in keywords:
            return ['']*13, ''
    addr_rest = ' '.join(addr_rest)
    return get_addr(new), addr_rest

def get_nosuffix_addr(s):
    """
    Breaks down a cleaned [urban] address with no street suffix into its component parts.
    :param s: cleaned address field (returned from addr_processing)
    :return: ['', unit, street_num, street_name, '', drxn, '', '', '', '', '', '', '']
    """
    mo = nosuffixRegex.search(s)
    if mo is None:
        return False
    g = list(mo.groups())
    # if the street name is now a suffix abbreviation, return False( e.g. "7275 St-Urbain, Suite 100")
    if g[2] in street_abbr.values():
        return False
    unit, street_num, drxn = '', '', ''
    if g[1] is not None:
        unit = g[0][:-1]
        street_num = g[1][:-1]
    else:
        street_num = g[0][:-1]
    street_name = g[2]
    if street_name.isdigit():  # street name can't just be a number in this case
        return False
    if g[3] is not None:
        drxn = g[3][-1]
    return ['', unit, street_num, street_name, '', drxn, '', '', '', '', '', '', '']

def addressParse(addr, fmt=None, extra=False):
    addr, floor, pobox, bldg, careof = addr_processing(addr)
    addr_lst = False
    addr_rest = ''
    if fmt is None:
        addr_lst = get_addr(addr)
        if addr_lst == False:
            addr_lst = get_rural_addr(addr)
            if addr_lst == False:
                addr_lst = get_nosuffix_addr(addr)
                if addr_lst == False:
                    addr_lst, addr_rest = get_extrainfo_addr(addr)
                    if addr_lst == [''] * 13:
                        addr_lst = False
    elif fmt == 'urban':
        addr_lst = get_addr(addr)
    elif fmt == 'rural':
        addr_lst = get_rural_addr(addr)
    elif fmt == 'nosuffix':
        addr_lst = get_nosuffix(addr)
    elif fmt == 'extra':
        addr_lst, addr_rest = get_extrainfo_addr(addr)
    else:
        raise ValueError('Unknown format specified: %s' % fmt)
    
    if addr_lst == False:
        return False
    fields = ['unit_type','unit','street_num','street_name','suffix','drxn','rr',
              'lot','site','comp','stn','lcd','rpo','floor','pobox','careof']
    d = dict(zip(fields, addr_lst))
    if addr_lst and extra:
        d['addr_rest'] = addr_rest
    return d
