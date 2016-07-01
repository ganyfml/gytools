#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\t2\nc\t4\n" | awk '{ printf("%s\t%.2f\n", $1, $2) }'

