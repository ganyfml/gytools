#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "a\nb\n"
printf "a\nb\n" | awk '{ print $0; exit }'
