#!/usr/bin/env python

import json
import urllib2
import requests

def count_numLinesInFile(file_name):
    file = open(file_name, 'r')
    num_lines = sum(1 for line in file)
    return num_lines

REST_URL = "http://www.ebi.ac.uk/arrayexpress/json/v2/experiments?keywords="
filter = "&organism=Homo+sapiens&exptype%5B%5D=\"rna+assay\"&exptype%5B%5D=\"array+assay\"&array="

disease_list = raw_input('Enter the disease list file name:>')
result_list = raw_input('Enter the result output file name:>')

num_lines = count_numLinesInFile(disease_list)
num_linesSearchSoFar = 0

disease = open(disease_list,'r')
result = open(result_list,'wb')

for line in disease:
    num_linesSearchSoFar += 1
    currentline = line.rstrip('\n')
    print REST_URL+urllib2.quote(currentline)+filter
    print "Requesting for disease: " + currentline
    r = requests.get(REST_URL+urllib2.quote(currentline.replace("/", " "))+filter)
    number_result = r.json()['experiments']['total']
    print "Number of experiment found: " + `number_result`
    print "Progress: " + `num_linesSearchSoFar` + "/" + `num_lines` + '\n'
    if number_result > 0:
        result.write(currentline+","+`number_result`+"\n")
