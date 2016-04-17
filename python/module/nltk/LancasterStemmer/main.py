#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from nltk.stem.lancaster import LancasterStemmer

if __name__ == '__main__':
	print LancasterStemmer().stem('lovely')
