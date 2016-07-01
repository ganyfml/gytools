#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\tb\nc\td\n" 
printf "a\tb\nc\td\n" | awk 'BEGIN { RS = "\t" } { print }' # set "RS" variable to change the definition of a "line".
