#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import requests
from collections import defaultdict

organsim = sys.argv[1]
technology = sys.argv[2]
molecule = sys.argv[3]

for search_term in sys.stdin:
	params_name = ['keywords', 'organism', 'exptype', 'exptype']
	params_value = [search_term, organsim, technology, molecule]
	params = defaultdict(list)
	for n, v in zip(params_name, params_value):
		if v:
			params[n].append(v)

	request_url = requests.Request(
			method = 'GET'
			, url = 'http://www.ebi.ac.uk/arrayexpress/json/v2/experiments'
			, params = params
			).prepare().url
	experiments_in_json = requests.get(request_url).json()['experiments']
	num_result = experiments_in_json['total']
	if num_result == 1:
		print experiments_in_json['experiment']['accession']
	else:
		for exp_id in xrange(num_result):
			print experiments_in_json['experiment'][exp_id]['accession']
