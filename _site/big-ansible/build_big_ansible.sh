#!/bin/sh

id=1
name=big-ansible
image=amelon1/${name}

docker build \
    -t $image:$id \
    -t $image:latest \
    -f Dockerfile \
    .

