#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\tb\nc\td\n" 
printf "a\tb\nc\td\n" | awk 'BEGIN { ORS = "\t" } { print }' # the default output separator is a newline
