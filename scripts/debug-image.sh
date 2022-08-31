#!/bin/bash

set -e

function check_requirements() {
  if [[ -z "$REGISTRY_USERNAME" ]]; then
    echo "Please provide an environment variable 'REGISTRY_USERNAME' for debugging the image."
    exit 1
  elif [[ -z "$IMAGE_NAME" ]]; then
    echo "Please provide an environment variable 'IMAGE_NAME' for debugging the image."
    exit 1
  elif [[ -z "$TAG" ]]; then
    echo "Please provide an environment variable 'TAG' for debugging the image."
    exit 1
  elif [[ -z "$PORT" ]]; then
    echo "Please provide an environment variable 'PORT' for debugging the image."
    exit 1
  fi
}

function main() {
  check_requirements

  docker run --interactive --tty \
    --env PORT=$PORT \
    --network shopping-cart-service_shopping-cart-network \
    --publish $PORT:$PORT \
    $REGISTRY_USERNAME/$IMAGE_NAME:$TAG
}

main
