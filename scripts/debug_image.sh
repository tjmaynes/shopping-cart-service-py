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
elif [[ -z $DATABASE_URI ]]; then
    echo "Please provide a uri for accessing the database."
    exit 1
elif [[ -z $FLASK_APP ]]; then
    echo "Please provide an entrypoint to the api service."
    exit 1
fi

docker run --rm \
    --env DATABASE_URI=$DATABASE_URI \
    --env FLASK_APP=$FLASK_APP \
    --publish 5000:5000 \
     $REGISTRY_USERNAME/$IMAGE_NAME:$TAG
