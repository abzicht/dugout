#!/bin/sh

function ssh_repeater () {
	# rerun ssh as soon as the existing connection fails
	while true
	do
		ssh -N -i $WORK/id_rsa -L 127.0.0.01:4321:127.0.0.1:4321 -o "ServerAliveInterval 120" -o "StrictHostKeyChecking no" $SSHUSER@$SSHSERVER;
		echo "SSH connection failed. Establishing new connection."
	done
}

ssh_repeater &

dugout-crawler $WORK/config.json -i 5 -v 2
