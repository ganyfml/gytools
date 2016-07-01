#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v 
awk 'BEGIN { print split("123&456&789", file, "&") }'
awk 'BEGIN { n = split("123&456&789", file, "&"); for(i = 1; i <= n; i++) print file[i] }'

