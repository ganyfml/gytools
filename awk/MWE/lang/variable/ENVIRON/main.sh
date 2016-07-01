#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
export test='aaaaaa'

awk 'BEGIN { print ENVIRON["test"] }'
