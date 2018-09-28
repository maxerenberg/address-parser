# address-parser
An address parser built in Python.  
Usage:  
```
>>> from addressParse import addressParse
>>> from pprint import pprint
>>> pprint(addressParse('101-11234 West 12th Avenue'))
{'comp': '',
 'drxn': '',
 'lcd': '',
 'lot': '',
 'rpo': '',
 'rr': '',
 'site': '',
 'stn': '',
 'street_name': 'W 12TH',
 'street_num': '11234',
 'suffix': 'AVE',
 'unit': '101',
 'unit_type': ''} 
 ```
 If the format of the address is known (possible values: 'urban', 'rural', 'nosuffix' (no street suffix),  
 'extra' (extra info included in address)):  
 ```
 >>> pprint(addressParse('3757 Anchor Way RR2', fmt='rural'))
 {'comp': '',
 'drxn': '',
 'lcd': '',
 'lot': '',
 'rpo': '',
 'rr': '2',
 'site': '',
 'stn': '',
 'street_name': 'ANCHOR',
 'street_num': '3757',
 'suffix': 'WAY',
 'unit': '',
 'unit_type': ''}
 ```
 To show the non-parsed parts of the address, if any:  
 ```
 >>> pprint(addressParse('234 Island Highway, Bowser, BC, V0R 1G0', extra=True))
 {'addr_rest': 'BOWSER BC V0R 1G0',
 'comp': '',
 'drxn': '',
 'lcd': '',
 'lot': '',
 'rpo': '',
 'rr': '',
 'site': '',
 'stn': '',
 'street_name': 'ISLAND',
 'street_num': '234',
 'suffix': 'HWY',
 'unit': '',
 'unit_type': ''}
 ```
 Returns ```False``` if address could not be parsed.
 Currently only works for anglophone addresses.
