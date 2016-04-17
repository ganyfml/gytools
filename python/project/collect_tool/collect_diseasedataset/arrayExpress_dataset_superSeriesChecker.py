#!/usr/bin/env python
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import requests
import sys

NCBI_Query = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="

def print_is_superSeries(name_dataset):
	GSE_name = "GSE" + name_dataset.split('-')[-1]
	result_page = requests.get(NCBI_Query + GSE_name).text
	print "This SuperSeries is composed of the following SubSeries:" in result_page

def get_is_superSeries(name_dataset):
	GSE_name = "GSE" + name_dataset.split('-')[-1]
	result_page = requests.get(NCBI_Query + GSE_name).text
	return "This SuperSeries is composed of the following SubSeries:" in result_page

def main():
	for line in sys.stdin:
		print_is_superSeries(name_dataset)
