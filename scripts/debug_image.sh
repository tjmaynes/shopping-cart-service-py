#!/bin/sh

set -e

DB_HOST=$1
DB_USERNAME=$2
DB_PASSWORD=$3
DB_NAME=$4
DB_PORT=$5
SERVER_PORT=$6
REGISTRY_USERNAME=$7
IMAGE_NAME=$8
TAG=$9

if [[ -z $DB_HOST ]]; then
    echo "Please provide a host for the database."
    exit 1
elif [[ -z $DB_NAME ]]; then
    echo "Please provide a name for the database."
    exit 1
elif [[ -z $DB_PORT ]]; then
    echo "Please provide a port that the database is running on."
    exit 1
elif [[ -z $DB_USERNAME ]]; then
    echo "Please provide a username for connecting to the database."
    exit 1
elif [[ -z $DB_PASSWORD ]]; then
    echo "Please provide a password for connecting to the database."
    exit 1
elif [[ -z $SERVER_PORT ]]; then
    echo "Please provide a port to run the image on."
    exit 1
elif [[ -z $REGISTRY_USERNAME ]]; then
    echo "Please provide a registry username for the image."
    exit 1
elif [[ -z $IMAGE_NAME ]]; then
    echo "Please provide an image name for the image."
    exit 1
elif [[ -z $TAG ]]; then
    echo "Please provide an tag for the image."
    exit 1
fi

docker run --rm \
    --env PYTHON_CART_DB_HOST=$DB_HOST \
    --env PYTHON_CART_DB_NAME=$DB_NAME \
    --env PYTHON_CART_DB_PORT=$DB_PORT \
    --env PYTHON_CART_DB_USERNAME=$DB_NAME \
    --env PYTHON_CART_DB_PASSWORD=$DB_PASSWORD \
    --network $IMAGE_NAME-network \
    --publish $SERVER_PORT:$SERVER_PORT \
     $REGISTRY_USERNAME/$IMAGE_NAME:$TAG
