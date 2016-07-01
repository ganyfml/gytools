#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\t5\nb\t3\n" 
printf "a\t5\nb\t3\n" | awk '{ for ( i = 1; i <= $2; i = i + 2 ) print $1 }'
