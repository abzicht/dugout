#!/bin/sh
ssh -L 127.0.0.01:$PORT:127.0.0.1:$PORT $SSHUSER@$SSHSERVER
dugout-crawler $WORK/config.json -i 5 -v 3
