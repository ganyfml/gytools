#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
../twogramsFreq.py <<EOF
NLTK is a leading platform for building Python programs to work with human language data.
It provides easy-to-use interfaces-α to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.
EOF

../twogramsFreq.py <<< the
../twogramsFreq.py <<< 'xxxx yyyy xxxx yyyy xxxx yyyy xxxx yyyy xxxx yyyy'
