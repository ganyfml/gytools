#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
awk -e 'BEGIN { print substr("abcdf", 2) }'
awk -e 'BEGIN { print substr("abcdf", 2, 1) }'
