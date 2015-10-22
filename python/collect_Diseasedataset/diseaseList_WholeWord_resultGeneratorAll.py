#!/usr/bin/env python

import json
import urllib2
import requests


REST_URL = "http://www.ebi.ac.uk/arrayexpress/json/v2/experiments?keywords="
filter_seq = "&organism=Homo+sapiens&exptype%5B%5D=\"rna+assay\"&exptype%5B%5D=\"sequencing+assay\"&array="
filter_array = "&organism=Homo+sapiens&exptype%5B%5D=\"rna+assay\"&exptype%5B%5D=\"array+assay\"&array="
NCBI_Query = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="

def count_numLinesInFile(file_name):
    file = open(file_name, 'r')
    num_lines = sum(1 for line in file)
    return num_lines

def is_superSeries(name_dataset):
    query_name = "GSE" + name_dataset.split('-')[-1]
    result = requests.get(NCBI_Query + query_name).text
    if "This SuperSeries is composed of the following SubSeries:" not in result:
        return False
    return True

def getJson_resultFromDisease(disease, type):
    if type == 'Array':
        r = requests.get(REST_URL+urllib2.quote(disease.replace("/", " "))+filter_array).json()
    elif type == 'Seq':
        r = requests.get(REST_URL+urllib2.quote(disease.replace("/", " "))+filter_seq).json()
    return r

def get_diseaseDisplayName(name):
    return name.rstrip('\n')

def get_diseaseQueryName(line):
    return '"' + line.rstrip('\n') + '"'

def write_oneTypeResult(number_result, result_json, type_result, file_write):
    if number_result == 1:
        data_set = result_json['experiments']['experiment']['accession']
        print_result = data_set + ',' + type_result
        if is_superSeries(data_set) == True:
            print_result += ',SuperSeries'
        file_write.write(print_result + "\n")
    else:
        for exp_id in range(number_result):
            data_set = result_json['experiments']['experiment'][exp_id]['accession']
            print_result = data_set + ',' + type_result
            if is_superSeries(data_set) == True:
                print_result += ",SuperSeries"
            file_write.write(print_result + "\n")
            file_write.write(',')


def write_result(disease, result_arrayJSON, result_seqJSON, file_write):
    num_resultArray =  result_arrayJSON['experiments']['total'] 
    num_resultSeq = result_seqJSON['experiments']['total']
    if num_resultArray + num_resultSeq > 0:
        file_write.write(disease + ",")
        write_oneTypeResult(num_resultSeq, result_seqJSON, "Seq Data", file_write)
        write_oneTypeResult(num_resultArray, result_arrayJSON, "Array Data", file_write)
        file_write.write('\n')

disease_list = raw_input('Enter the disease list file name:>')
result_list = raw_input('Enter the result output file name:>')
num_lines = count_numLinesInFile(disease_list)
num_linesSearchSoFar = 0
disease = open(disease_list,'r')
result = open(result_list,'wb')

for line in disease:
    num_linesSearchSoFar += 1
    disease_name = get_diseaseDisplayName(line)
    print "Requesting for disease: " + disease_name 
    result_arrayJSON = getJson_resultFromDisease(get_diseaseQueryName(line), 'Array')
    result_seqJSON = getJson_resultFromDisease(get_diseaseQueryName(line), 'Seq')
    write_result(disease_name, result_arrayJSON, result_seqJSON, result)
    print "Progress: " + `num_linesSearchSoFar` + "/" + `num_lines`
