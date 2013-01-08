#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, json

with open('./country-codes.json', 'rU') as f:
    country_codes = json.load(f)

def search_country_names(pat):
    for country in country_codes:
        if not re.search(pat, country['name'], re.I): continue
        yield country

if __name__ == '__main__':
    pat = sys.argv[1]
    for country in search_country_names(pat):
        print json.dumps(country, indent=4, separators=(',', ':\t'))
    
