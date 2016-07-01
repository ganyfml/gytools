#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "it is meaningless it" | awk '{ print gsub("it", "It"); print }'
printf "it is meaningless it" | awk '{ print gsub("it", "It", $1); print }'
