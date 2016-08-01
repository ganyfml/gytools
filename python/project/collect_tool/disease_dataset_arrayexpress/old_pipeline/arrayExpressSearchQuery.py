#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import json
import requests
from collections import defaultdict

organsim = sys.argv[1]
technology = sys.argv[2]
molecule = sys.argv[3]

def get_platform(experiment):
	if 'arraydesign' in experiment: 
		if not isinstance(experiment['arraydesign'],list):
			return experiment['arraydesign']['name']
		else:
			return ' / '.join([design['name'] for design in experiment['arraydesign']])
	else:
		return 'Unknown'

def is_superSeries(name_dataset):
	query_name = "GSE" + name_dataset.split('-')[-1]
	result = requests.get('http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + query_name).text
	return "This SuperSeries is composed of the following SubSeries:" in result

def get_info_forOneDataSet(dataset, disease, organsim, technology):
	dataset_title = dataset['name']
	return '\t'.join([
		disease
		, dataset['accession']
		, str(dataset['samples'])
		, organsim
		, technology
		, get_platform(dataset)
		, dataset_title
		, str(is_superSeries(dataset['accession']))
		]).encode('utf-8')

def get_resultOne(search_entry, organsim, technology, molecule):
	params_name = ['keywords', '"organism"', '"exptype"', '"exptype"']
	params_value = [search_entry, organsim, technology, molecule]
	params = defaultdict(list)
	for n, v in zip(params_name, params_value):
		if v:
			params[n].append(v)
	request_url = requests.Request('GET'
			, 'http://www.ebi.ac.uk/arrayexpress/json/v2/experiments'
			, params = params
			).prepare().url
	result_json = requests.get(request_url).json()
	json_experiments = result_json['experiments']
	num_result = json_experiments['total']
	if num_result == 1:
		dataset = json_experiments['experiment']
		print get_info_forOneDataSet(dataset, search_entry.strip('"'), organsim, technology)
	else:
		for exp_id in range(num_result):
			dataset = json_experiments['experiment'][exp_id]
			print get_info_forOneDataSet(dataset, search_entry.strip('"'), organsim, technology)

for line in sys.stdin:
	get_resultOne('"' + line.rstrip('\n') + '"', organsim, technology, molecule)
