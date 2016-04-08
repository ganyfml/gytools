#!/usr/bin/env python
# vim: set noexpandtab tabstop=2:

from nltk.corpus import wordnet
import operator

disease_dict = {}
drug_dict = {}

with open('disease_data.tsv', 'r') as disease_data:
		for d in disease_data:
				(key, value) = d.split('\t')
				value = int(value)
				disease_dict[key] = value
sorted_disease = dict(sorted(disease_dict.items(), key=operator.itemgetter(1), reverse=True)[:1000])

with open('drug_data.tsv', 'r') as drug_data:
		for d in drug_data:
				(key, value) = d.split('\t')
				value = int(value)
				drug_dict[key] = value
sorted_drug = dict(sorted(drug_dict.items(), key=operator.itemgetter(1), reverse=True)[:1000])

with open('compare_result.tsv', 'w+') as result:
		for drug_word in sorted_drug.iterkeys():
				if drug_word in sorted_disease:
						result.write('\t'.join([drug_word, str(disease_dict[drug_word]), str(drug_dict[drug_word])]) + '\n')
