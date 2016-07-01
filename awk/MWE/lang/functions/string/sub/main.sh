#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "it is meaningless it" | awk '{ print sub("it", "It"); print }'
# only convert first one and the default is $0
printf "it is meaningless it" | awk '{ print sub("it", "It", $2); print }'
