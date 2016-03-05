#!/usr/bin/env python

import json
import requests
import sys

REST_URL = "http://www.ebi.ac.uk/arrayexpress/json/v2/experiments?keywords="
ORGANSIM = ['Homo+sapiens', 'Mus+musculus']
TECHNOLOGY = ['\"sequencing+assay\"', '\"array+assay\"']
NCBI_Query = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="

def form_searchQuery(search_entry, organsim_index, technology_index):
    searchfilter = '&organism=' + ORGANSIM[organsim_index] + '&exptype%5B%5D=\"rna+assay\"&exptype%5B%5D=' + TECHNOLOGY[technology_index] + '&array='
    query = REST_URL + search_entry + searchfilter
    return query

def get_platform(experiment):
    platform = ''
    if 'arraydesign' in experiment: 
        if not isinstance(experiment['arraydesign'],list):
            platform = experiment['arraydesign']['name']
        else:
            for design_index in range(len(experiment['arraydesign'])):
                platform += experiment['arraydesign'][design_index]['name']
                if design_index != (len(experiment['arraydesign']) - 1):
                    platform += ' / '
    else:
        platform = "Unknown"
    return platform

def is_superSeries(name_dataset):
    query_name = "GSE" + name_dataset.split('-')[-1]
    result = requests.get(NCBI_Query + query_name).text
    if "This SuperSeries is composed of the following SubSeries:" not in result:
        return False
    return True

def get_resultOne(search_entry, organsim_index, technology_index):
    result_json = requests.get(form_searchQuery(search_entry, organsim_index, technology_index)).json()
    num_result = result_json['experiments']['total']
    if num_result == 1:
        dataset = result_json['experiments']['experiment']['accession']
        platform = get_platform(result_json['experiments']['experiment'])
        result = dataset + '\t' + platform
        if is_superSeries(dataset) == True:
            result += '\tSuperSeries'
        result = result.encode('ascii', 'ignore')
        print result
    else:
        for exp_id in range(num_result):
            dataset = result_json['experiments']['experiment'][exp_id]['accession']
            platform = get_platform(result_json['experiments']['experiment'][exp_id])
            result = dataset + '\t' + platform
            if is_superSeries(dataset) == True:
                result += ",SuperSeries"
            result = result.encode('ascii', 'ignore')
            print result

for line in sys.stdin:
    get_resultOne(line, int(sys.argv[1]), int(sys.argv[2]))
