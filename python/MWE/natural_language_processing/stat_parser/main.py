#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
from stat_parser import Parser

parser = Parser()
print 'Init complete'
print parser.parse(sys.argv[1])
