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

def get_abstracts(paper_ids):
		result = requests.get(URL.replace('ARTICLEID', paper_ids)).text.encode('ascii', 'ignore')
		abstracts = ET.fromstring(result).findall('.//AbstractText')
		return abstracts

def get_words_from_paper(paper_ids, word_collection):
		stops = set(stopwords.words('english'))
		abstracts = get_abstracts(paper_ids)
		for a in abstracts:
				tokens = nltk.word_tokenize(a.text)
				for word in tokens:
						word = word.lower()
						if re.match('[a-z0-9]', word) and word.lower() not in stops:
								word_collection[word] += 1

input_file = str(sys.argv[1])
output_file = input_file.split('.')[0] + '.tsv'

word_collection = defaultdict(lambda: 0)
paper_ids = []
with open(input_file, 'r') as diseases:
		total_line = sum(1 for line in diseases)
		current_line = 0
		diseases.seek(0)
		for d_id in diseases:
				paper_ids.append(d_id)
				current_line += 1
				if current_line % 1000 == 0 or current_line == total_line:
						get_words_from_paper('.'.join(paper_ids), word_collection)
						print("processing: {0}/{1}").format(current_line, total_line)
						paper_ids = []

sorted_word = sorted(word_collection.items(), key=operator.itemgetter(1), reverse=True)
with open(output_file, 'w+') as save_file:
		for word,count in sorted_word:
				save_file.write('\t'.join([word, str(count)]) + "\n")
