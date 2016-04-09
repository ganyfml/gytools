#!/usr/bin/env python
# vim: set noexpandtab tabstop=2:

import sys
import requests
import xml.etree.ElementTree as ET

URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="

def get_list_length(search_term):
		result = requests.get(URL + search_term).text.encode('ascii', 'ignore')
		length = ET.fromstring(result).find('.//Count').text
		return length

def get_full_list(search_term, length):
		search_url = URL + search_term + "&RetMax=" + length
		result = requests.get(search_url).text.encode('ascii', 'ignore')
		full_list = ET.fromstring(result).findall('.//Id')
		return full_list

def main(search_term):
		num_paper = get_list_length(search_term)
		papers_id = get_full_list(search_term, num_paper)
		with open(search_term + '.list', 'w+') as output:
				for p in papers_id:
						output.write(p.text + '\n')

search_term = str(sys.argv[1])
main(search_term)
