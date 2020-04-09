#!/bin/bash

set -e

REGISTRY_USERNAME=$1
IMAGE_NAME=$2
TAG=$3

if [[ -z $REGISTRY_USERNAME ]]; then
    echo "Please provide a registry username for the image."
    exit 1
elif [[ -z $IMAGE_NAME ]]; then
    echo "Please provide an image name for the image."
    exit 1
elif [[ -z $TAG ]]; then
    echo "Please provide an tag for the image."
    exit 1
fi

docker build -t $REGISTRY_USERNAME/$IMAGE_NAME:$TAG .
