#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

tmpdir=$(mktemp -d)
../gmlgencred.py clientsecrets.json "$tmpdir/credential.json"
echo "$tmpdir"
