#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a|3" | awk '{ print $1 }'
printf "a|3" | awk 'BEGIN { FS = "|" } { print $1 }' #FS = field separator
