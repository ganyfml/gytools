#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

from nltk.corpus import stopwords

if __name__ == '__main__':
	print set(stopwords.words('english'))
