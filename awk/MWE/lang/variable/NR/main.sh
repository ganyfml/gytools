#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\tb\nc\td\ne\tf\tg\n" | awk '{print NR "\t" $0}' # NR: count the lines in a file; $0: each line
