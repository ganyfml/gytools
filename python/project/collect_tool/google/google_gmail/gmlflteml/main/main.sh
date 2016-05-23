#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

set -v
printf "%s\n" 'Robert.Roeder@rockefeller.edu' 'xxx@yyy.zzz' | ../gmlflteml.py "$(readlink -f -e ~/.credentials/pengyu.bio@gmail.com.json)" 'yes'
printf "%s\n" 'Robert.Roeder@rockefeller.edu' 'xxx@yyy.zzz' | ../gmlflteml.py "$(readlink -f -e ~/.credentials/pengyu.bio@gmail.com.json)" 'no'
