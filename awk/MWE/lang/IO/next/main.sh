#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\nc\td\ne\tf\n" 
printf "a\nc\td\ne\tf\n" | awk '{ if (NR == 1) {next} print }'
