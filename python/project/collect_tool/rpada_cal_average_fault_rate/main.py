#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys

def cal_average_false_rate(grade_file):
	num_student = 0
	rate_sum = 0
	with open(grade_file, 'r') as f:
		for line in f:
			if 'num of wrong' in line:
				num_wrong = float(line.split(' ')[-1])
				if num_wrong > 10:
					continue
				rate_sum += num_wrong / 20
				num_student += 1
	print grade_file
	print rate_sum / num_student

for grade_file in sys.stdin.readlines():
	cal_average_false_rate(grade_file.rstrip())
