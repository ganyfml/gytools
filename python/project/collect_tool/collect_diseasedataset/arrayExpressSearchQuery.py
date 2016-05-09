#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import codecs
import locale
import json
import requests

ORGANSIM = ['Homo sapiens', 'Mus musculus']
TECHNOLOGY = ['sequencing assay', 'array assay']

def get_platform(experiment):
	if 'arraydesign' in experiment: 
		if not isinstance(experiment['arraydesign'],list):
			return experiment['arraydesign']['name']
		else:
			platform = ''
			for design_index in range(len(experiment['arraydesign'])):
				platform += experiment['arraydesign'][design_index]['name']
				if design_index != (len(experiment['arraydesign']) - 1):
					platform += ' / '
			return platform
	else:
		return 'Unknown'

def is_superSeries(name_dataset):
	query_name = "GSE" + name_dataset.split('-')[-1]
	result = requests.get('http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + query_name).text
	return "This SuperSeries is composed of the following SubSeries:" in result

def get_info_forOneDataSet(dataset, disease, organsim_index, technology_index):
	dataset_title = dataset['name']
	dataset_num_sample = str(dataset['samples'])
	try:
		ret = '\t'.join([
			disease
			, dataset['accession']
			, dataset_num_sample
			, ORGANSIM[organsim_index]
			, TECHNOLOGY[technology_index]
			, get_platform(dataset)
			, dataset_title.encode('utf-8')
			, str(is_superSeries(dataset['accession']))
			]).encode('utf-8')
	except:
		print dataset['accession'] + ", " + disease

	return ret

def get_resultOne(search_entry, organsim_index, technology_index):
	request_url = requests.Request('GET'
			, 'http://www.ebi.ac.uk/arrayexpress/json/v2/experiments'
			, params={'keywords': search_entry, 'organism': ORGANSIM[organsim_index], 'exptype': TECHNOLOGY[technology_index]}
			).prepare().url
	result_json = requests.get(request_url).json()
	json_experiments = result_json['experiments']
	num_result = json_experiments['total']
	if num_result == 1:
		dataset = json_experiments['experiment']
		print get_info_forOneDataSet(dataset, search_entry.strip('"'), organsim_index, technology_index)
	else:
		for exp_id in range(num_result):
			dataset = json_experiments['experiment'][exp_id]
			print get_info_forOneDataSet(dataset, search_entry.strip('"'), organsim_index, technology_index)

organsim_index = sys.argv[1]
technology_index = sys.argv[2]

for line in sys.stdin:
	get_resultOne('"' + line.rstrip() + '"', int(organsim_index), int(technology_index))
