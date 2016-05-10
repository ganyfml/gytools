#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import nltk
import sys

lemmatizer = nltk.WordNetLemmatizer()
def normalise(word):
	if word.isupper():
		return word
	else:
		return lemmatizer.lemmatize(word.lower())

from nltk.corpus import stopwords
stopwords = stopwords.words('english')
def acceptable_word(word):
	import string
	return bool(
		2 <= len(word) <= 40
		and word.lower() not in stopwords
		and filter(lambda x: x not in string.punctuation, word))

def leaves(tree):
	for subtree in tree.subtrees(filter = lambda t: t.label() == 'NP'):
		yield subtree.leaves()

def get_terms(text):
	tokens = nltk.word_tokenize(text)
	postokens = nltk.tag.pos_tag(tokens)
	
	grammar = r"""
			NBAR:
					{<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
	
			NP:
					{<NBAR>}
					{<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
			"""
	chunker = nltk.RegexpParser(grammar)
	tree = chunker.parse(postokens)
	
	for leaf in leaves(tree):
		term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
		if len(term) != 0:
			yield term

from collections import defaultdict
result_map = defaultdict(int)
num_line_processed = 0
for line in sys.stdin.readlines():
	num_line_processed += 1
	terms = get_terms(line.decode('utf-8'))
	for term in terms:
		t = ' '.join(term).encode('utf-8')
		result_map[t] += 1
	
import operator
final_result = sorted(result_map.items(), key= operator.itemgetter(1), reverse = True)
for result in final_result:
	print '\t'.join(str(e) for e in result)
