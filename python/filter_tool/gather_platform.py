#!/usr/bin/env python

import operator

file_name = 'whole_rare_disease_list_result.tsv'

platform = {}
file = open(file_name, 'r')
for line in file:
    temp_platforms = line.split('\t')[5]
    temp_platform = temp_platforms.split('/')
    for p in temp_platform:
        p = p.strip()
        if(platform.has_key(p)):
            platform[p] += 1
        else:
            platform[p] = 1

result_file = open('platform_info.tsv', 'w+')
sorted_platform_iter = iter(sorted(platform.items(), key=operator.itemgetter(1), reverse=True))
for item in sorted_platform_iter:
    line = item[0]+ '\t' + str(item[1]) + '\n'
    result_file.write(line)
