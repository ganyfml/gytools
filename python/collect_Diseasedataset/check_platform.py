#!/usr/bin/env python

import json
import urllib2
import requests
import sys

REST_URL = "http://www.ebi.ac.uk/arrayexpress/json/v2/experiments/"

result_json = requests.get(REST_URL + sys.argv[1]).json()

if 'experiment' not in result_json['experiments']:
    print "No such dataset"
    exit()

platform = ""
if 'arraydesign' in result_json['experiments']['experiment']:
    array_design = result_json['experiments']['experiment']['arraydesign']
    if not isinstance(array_design,list):
        platform = arraydesign['name']
    else:
        for design_index in range(len(array_design)):
            platform += array_design[design_index]['name'] + "/"
else:
    platform = "Unknown"

print platform
