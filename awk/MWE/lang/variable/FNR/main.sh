#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\tb\nc\td\n" > a
printf "e\tf\ng\th\n" > b
awk '{print FNR "\t" $0}' a b
awk '{print NR "\t" $0}' a b
