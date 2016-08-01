#!/usr/bin/env python

source_list = raw_input('Enter the source file name:>')
ref_list = raw_input('Enter the ref file name:>')
result_list = raw_input('Enter the result name:>')
source = open(source_list, 'r')
result = open(result_list, 'wb')

for line in source:
    disease_name = line.split('\t')[0].split(" ")
    is_rare = False
    for component in disease_name:
        if component != "Syndrome" and component != "Disease" and component != "Disorder" :
            if component in open(ref_list, 'r').read():
                is_rare = True
                break
    if is_rare == True :
        result.write(line)
