#!/usr/bin/env python
# vim: set noexpandtab tabstop=2:

import sys
import requests
import re
import xml.etree.ElementTree as ET
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
import operator

URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=ARTICLEID&retmode=xml"
stop_words = set(stopwords.words('english'))

def get_words_and_titles(paper_ids, result_list):
		result = requests.get(URL.replace('ARTICLEID', str(paper_ids))).text.encode('ascii', 'ignore')
		articles = ET.fromstring(result).findall('.//PubmedArticle')
		local_result = defaultdict(lambda: (0, set()))
		for a in articles:
				try:
						tokens = nltk.word_tokenize(a.find('.//AbstractText').text)
						title = a.find('.//ArticleTitle').text
						for word in tokens:
								word = word.lower()
								if re.match('[a-z0-9]', word) and word.lower() not in stop_words:
										local_result[word][0] += 1
										local_result[word][1].add(title)
				except:
						pass
		result_list.update(local_result)

def write_result_to_file(output_file, result_list):
		with open(output_file, 'w+') as save_file:
				for word, info in result_list:
						for title in info[1]:
								save_file.write('\t'.join([word, str(info[0]), title]) + "\n")

def main(input_file):
		result_list = {}
		with open(input_file, 'r') as papers:
				current_line = 0
				total_line = sum(1 for line in papers)
				papers.seek(0)
				paper_ids = []
				for s in papers:
						paper_ids.append(s)
						current_line += 1
						if current_line % 1000 == 0 or current_line == total_line:
								get_words_and_titles(paper_ids, result_list)
								paper_ids = []
								print("processing: {0}/{1}").format(current_line, total_line)

		output_file = input_file.split('.')[0] + '.tsv'
		write_result_to_file(output_file, result_list)

input_file = str(sys.argv[1])
main(input_file);
