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

dataset_json = json.load(sys.stdin)

def get_platform(experiment):
	if 'arraydesign' in experiment: 
		if not isinstance(experiment['arraydesign'],list):
			return experiment['arraydesign']['name']
		else:
			return ' / '.join([design['name'] for design in experiment['arraydesign']])
	else:
		return 'Unknown'

def is_superSeries(experiment):
	query_name = "GSE" + experiment['accession'].split('-')[-1]
	result = requests.get('http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + query_name).text
	return str("This SuperSeries is composed of the following SubSeries:" in result)

def print_info_forDataSet(dataset_json):
	experiment = dataset_json['experiments']['experiment']
	print '\t'.join([
		experiment['organism']
		, experiment['experimenttype']
		, experiment['accession']
		, str(experiment['samples'])
		, get_platform(experiment)
		, experiment['name']
		, is_superSeries(experiment)
		]).encode('utf-8')

print_info_forDataSet(dataset_json)
