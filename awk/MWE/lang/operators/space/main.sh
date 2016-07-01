#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\nb\nc\n" | awk '{ print $1 " " $1}'

