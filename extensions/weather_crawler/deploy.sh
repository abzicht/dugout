#!/bin/bash
docker build -t dugout-weather-crawler  ./
docker stack deploy --compose-file docker-stack.yml dugout
