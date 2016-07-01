#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\t5\nb\t3\n" 
printf "a\t5\nb\t3\n" | awk '{ i = 1; while (i <= $2) { print $1; i = i + 2 } }'
