#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\t2\nc\t4\n" | awk 'END { print "First", "Second" } { print }'
