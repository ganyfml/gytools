#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
cat ./test | ../../accession_2_json_url.py
