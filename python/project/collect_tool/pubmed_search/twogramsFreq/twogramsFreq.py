#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:
import sys
import signal
#http://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
signal.signal(signal.SIGINT, lambda x,y: sys.exit(128 + signal.SIGINT))

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

from collections import defaultdict
d1 = defaultdict(int)
d2 = defaultdict(int)

import nltk
import string

from nltk.util import ngrams

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')

import string

for line in sys.stdin:
	line = line.rstrip('\n')
	tokens = [token.lower() for token in word_tokenize(line.decode('utf-8')) if not token.lower() in english_stopwords and not token in string.punctuation ]
	for token in tokens:
		d1[token] += 1 

	for ngram in ngrams(tokens, 2):
		d2[ngram] += 1 

total = sum(d1.itervalues())

from math import log
from fisher import pvalue
for k,v in d2.iteritems():
	AB = v
	A	= d1[k[0]]
	B	= d1[k[1]]
	mat = [AB, A-AB, B-AB, total-A-B+AB]
	p = pvalue(*mat).right_tail

	print ("%s\t%.20g\t%d" % (' '.join(k), p, v)).encode('utf-8')

