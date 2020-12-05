#!/bin/sh

echo "SHELL=/bin/sh
* * * * * /dugout-backup/backup.sh
" > /dugout-backup/scheduler.txt

crontab /dugout-backup/scheduler.txt
cron -f
