#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
text = sys.stdin.read().decode('utf-8')

import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

import re
print '\n'.join([re.sub('\s+', ' ', s.strip()) for s in tokenizer.tokenize(text)]).encode('utf8')
