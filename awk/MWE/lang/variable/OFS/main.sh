#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
awk -v OFS=: -e 'BEGIN {print "x", "y"}'
