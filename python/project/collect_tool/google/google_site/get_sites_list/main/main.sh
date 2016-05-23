#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
../get_sites_list.py '' /tmp/gdata/token
../get_sites_list.py tamu.edu /tmp/gdata/token
