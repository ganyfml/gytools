#!/usr/bin/env python

import codecs
import locale
import json
import requests
import sys

REST_URL = "http://www.ebi.ac.uk/arrayexpress/json/v2/experiments"
ORGANSIM = ['Homo sapiens', 'Mus musculus']
TECHNOLOGY = ['sequencing assay', 'array assay']
NCBI_Query = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="

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

def get_info_forOneDataSet(dataset, disease, organsim_index, technology_index):
    dataset_id = unicode(dataset['accession'])
    dataset_title = unicode(dataset['name'])
    dataset_num_sample = unicode(dataset['samples'])
    dataset_platform = unicode(get_platform(dataset))
    dataset_tech = unicode(TECHNOLOGY[technology_index])
    dataset_organsim = unicode(ORGANSIM[organsim_index])
    dataset_diseaseName = unicode(disease)
    dataset_superSeries = unicode(is_superSeries(dataset_id))
    info = '\t'.join([dataset_diseaseName, dataset_id, dataset_num_sample, dataset_organsim, dataset_tech, dataset_platform, dataset_title, dataset_superSeries])
    return info

def get_resultOne(search_entry, organsim_index, technology_index):
    request_url = requests.Request('GET',
            REST_URL,
            params={'keywords': search_entry, 'organism': ORGANSIM[organsim_index], 'exptype': TECHNOLOGY[technology_index]}
            ).prepare().url
    result_json = requests.get(request_url).json()
    num_result = result_json['experiments']['total']
    if num_result == 1:
        dataset = result_json['experiments']['experiment']
        print >> sys.stderr, '+++++' + dataset['accession']
        print get_info_forOneDataSet(dataset, search_entry.strip('"'), organsim_index, technology_index)
    else:
        for exp_id in range(num_result):
            dataset = result_json['experiments']['experiment'][exp_id]
            print >> sys.stderr, '+++++' + dataset['accession']
            print get_info_forOneDataSet(dataset, search_entry.strip('"'), organsim_index, technology_index)

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
reload(sys)  
sys.setdefaultencoding('utf8')
for line in sys.stdin:
    print >> sys.stderr, line
    get_resultOne('"' + line.rstrip() + '"', int(sys.argv[1]), int(sys.argv[2]))
