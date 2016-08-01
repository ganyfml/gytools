#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys

CATEGORY = ['name', 'Email Address', 'Website', 'Description', 'Address', 'Phone', 'Fax', '800 Number', 'TDD']
def print_tsv_format(line):
	info_dict = {e.split('\002')[0] : e.split('\002')[1] for e in line.split('\t')}
	info_list = [info_dict.get(c, 'NA').strip('\n') for c in CATEGORY]
	print '\t'.join(info_list)

print '\t'.join(CATEGORY)
for org_detail in sys.stdin:
	print_tsv_format(org_detail)
