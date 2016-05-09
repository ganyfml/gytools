#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import nltk
import sys

print nltk.word_tokenize(sys.argv[1])
