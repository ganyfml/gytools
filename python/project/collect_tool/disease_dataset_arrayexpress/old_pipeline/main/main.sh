#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
echo 'Rett syndrome' | ../arrayExpressSearchQuery.py 'Homo sapiens' '"array assay"' '"rna assay"'
echo 'Rett syndrome' | ../arrayExpressSearchQuery.py 'Homo sapiens' '"sequencing assay"' '"dna assay"'
echo 'Rett syndrome' | ../arrayExpressSearchQuery.py 'Homo sapiens' '' ''
