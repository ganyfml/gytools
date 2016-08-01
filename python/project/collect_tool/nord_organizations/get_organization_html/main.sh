#!/usr/bin/env bash
#vim: set noexpandtab tabstop=2:

cut -f 2 ../get_organization_list/main/org_list.tsv > org_url.tsv

function cmd {
local url=$1
local name=$(sed 's/^.\+organizations\/\(.*\)\/$/\1/' <<< "$url")
wget "$url" -O "$name.html"
}

#Export the function `cmd()` so that parallel can see
export -f cmd

cat ./org_url.tsv | parallel 'cmd {}'
