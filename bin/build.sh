#!/usr/bin/env bash
# Build a docker image
docker build -t pyengine/aws-power-state . --no-cache

docker tag pyengine/aws-power-state pyengine/aws-power-state:1.0
docker tag pyengine/aws-power-state spaceone/aws-power-state:1.0
