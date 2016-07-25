#!/usr/bin/env bash
#vim: set noexpandtab tabstop=2:

cat test_repos.txt | ../../list_notification_status.py "../cookie_file"
