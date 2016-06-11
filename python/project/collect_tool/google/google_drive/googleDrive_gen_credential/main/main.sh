#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

tmpdir=$(mktemp -d)
../googleDrive_gen_credential.py clientsecrets.json "$tmpdir/credential.json"
echo "$tmpdir"
