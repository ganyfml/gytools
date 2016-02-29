#!/usr/bin/env python

import operator

platform_filename = 'platform_info.tsv'

platform = []
platform_file = open(platform_filename, 'r')
for line in range(5):
    platform.append(platform_file.readline().split('\t')[0])

data_filename = 'whole_rare_disease_list_result.tsv'
data_file = open(data_filename, 'r')
result_filename = 'filtered_data.tsv'
result_file = open(result_filename, 'w+')
for line in data_file:
    temp_platforms = line.split('\t')[5]
    temp_platform = temp_platforms.split('/')
    write = False
    for p in temp_platform:
        p = p.strip()
        if(p in platform):
           write = True
           break
    if write:
        result_file.write(line)
