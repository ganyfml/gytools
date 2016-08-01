#!/usr/bin/env bash
#vim: set noexpandtab tabstop=2:

set -v

../../gen_login_cookie.py 'a' 'b' > ../cookie_file
../../gen_login_cookie.py 'gany.fml@gmail.com' 'Gybt199049#' > ../cookie_file
