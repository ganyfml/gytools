#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

#(?x) means allow comments
sentence_re = r'''(?x)      # set flag to allow verbose regexps
		([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
		| \w+(-\w+)*            # words with optional internal hyphens
		| \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
		| \.\.\.                # ellipsis
		| [][.,;"'?():-_`]      # these are separate tokens
'''

import nltk
import sys

print nltk.regexp_tokenize(sys.argv[1], sentence_re)
