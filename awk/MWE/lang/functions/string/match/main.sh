#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
awk 'BEGIN {print match("It is meaningless", "is"), RSTART, RLENGTH}'
