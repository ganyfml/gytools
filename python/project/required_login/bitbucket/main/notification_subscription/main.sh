#!/usr/bin/env bash
#vim: set noexpandtab tabstop=2:

cat "./test_repos.txt" | ../../list_notification_status.py "../cookie_file"
cat "./test_repos.txt" | ../../notification_subscription.py "../cookie_file" T T T T
cat "./test_repos.txt" | ../../list_notification_status.py "../cookie_file"
