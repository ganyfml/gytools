#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import re
import nltk
import operator
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

def get_stop_words():
	return map(LancasterStemmer().stem, set(stopwords.words('english')))

def get_words_fromParagraph(paragraph, stop_words, result_map):
	tokens = map(LancasterStemmer().stem, nltk.word_tokenize(paragraph))
	for w in tokens:
		if re.match('[a-z0-9]', w) and w not in stop_words:
			if w in result_map:
				result_map[w] += 1
			else:
				result_map[w] = 1

def print_list_tsv(list):
	for elements in list:
		print '\t'.join(str(e) for e in elements)

if __name__ == "__main__":
	stop_words = get_stop_words()
	result = {}
	for line in sys.stdin:
		get_words_fromParagraph(line, stop_words, result)
	sorted_result_list = sorted(result.items(), key= operator.itemgetter(1), reverse = True)
	print_list_tsv(sorted_result_list)
