#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
wget -qO- $(<test) | ../../accession_detail_from_json.py
