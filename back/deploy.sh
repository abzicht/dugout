#!/bin/bash
docker build -t dugout-backup  ./
docker stack deploy --compose-file docker-stack.yml dugout
