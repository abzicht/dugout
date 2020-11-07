#!/bin/sh
ssh -N -i $WORK/id_rsa -L 127.0.0.01:4321:127.0.0.1:4321 -o "ServerAliveInterval 120" -o "StrictHostKeyChecking no" $SSHUSER@$SSHSERVER &
dugout-crawler $WORK/config.json -i 5 -v 2
