#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\tb\nc\td\ne\tf\tg\n" 
printf "a\tb\nc\td\ne\tf\tg\n" | awk '{ print NF }' #Number of Fields in a record
