#!/usr/bin/env python
# vim: set noexpandtab tabstop=2:

import sys

def read_from_file(file_name):
		loaded_dict = {}
		with open(file_name, 'r') as f:
				for d in f:
						(key, value, title) = d.split('\t')
						value = int(value)
						loaded_dict[key] = value
		return loaded_dict

input_file = str(sys.argv[1])
read_from_file(input_file)

#with open('compare_result.tsv', 'w+') as result:
#		for drug_word in sorted_drug.iterkeys():
#				if drug_word in sorted_disease:
#						result.write('\t'.join([drug_word, str(disease_dict[drug_word]), str(drug_dict[drug_word])]) + '\n')
