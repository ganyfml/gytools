#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys

category = ['name', 'Email Address', 'Website', 'Description', 'Address', 'Phone', 'Fax', '800 Number', 'TDD']

def print_tsv_format(line):
	info_dict = {e.split('##')[0] : e.split('##')[1] for e in line.split('\t')}
	info_list = [info_dict.get(c, 'NA').strip('\n') for c in category]
	print '\t'.join(info_list)

print '\t'.join(category)
with open(sys.argv[1]) as f:
	for org_detail in f:
		print_tsv_format(org_detail)
