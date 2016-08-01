#!/usr/bin/env bash
#vim: set noexpandtab tabstop=2:

set -v 

../../list_notification_status.py "../cookie_file" < ./test_repos.txt
cat "./test_repos.txt" | ../../notification_subscription.py "../cookie_file" U F F U
cat "./test_repos.txt" | ../../list_notification_status.py "../cookie_file"
