#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
awk -e 'BEGIN { for (i in ARGV) print i, ARGV[i] }' a b
