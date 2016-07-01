#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\t2\nc\t4\n" | awk 'BEGIN { print "First", "Second" } { print }'
