#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v 
awk -e 'BEGIN { print index("abc12d", "12")}'
