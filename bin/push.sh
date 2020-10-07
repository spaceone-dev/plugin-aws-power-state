#!/usr/bin/env bash
# How to upload
./bin/build.sh

docker push pyengine/aws-power-state:0.9
#docker push spaceone/aws-power-state:1.0
