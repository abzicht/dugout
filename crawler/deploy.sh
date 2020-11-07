#!/bin/bash
docker build -t dugout-crawler  ./
docker stack deploy --compose-file docker-stack.yml dugout
