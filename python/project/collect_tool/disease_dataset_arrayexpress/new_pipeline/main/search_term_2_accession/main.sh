#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
../../search_term_2_accession.py 'Homo sapiens' '"array assay"' '"rna assay"' <<< '"Rett syndrome"' 
../../search_term_2_accession.py 'Homo sapiens' '"sequencing assay"' '"dna assay"' <<< '"Rett syndrome"' 
../../search_term_2_accession.py 'Homo sapiens' '' '' <<< '"Rett syndrome"' 
