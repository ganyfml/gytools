#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\t5\nb\t3\nc\t8\n" 
printf "a\t5\nb\t3\nc\t8\n" | awk -f ./if_else.awk
