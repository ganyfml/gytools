#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys

def get_all_org_info_category(line, category_list):
	for info_element in line.split('\t'):
		category_name = info_element.split('\002')[0]
		if category_name not in category_list:
			category_list.append(category_name)

for org_detail in sys.stdin:
	category_list = []
	get_all_org_info_category(org_detail, category_list)

print category_list
