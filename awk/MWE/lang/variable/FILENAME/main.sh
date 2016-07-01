#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf '111' > a
printf '222' > b
printf '333' > c
awk '{print FILENAME, $0}' a b c
