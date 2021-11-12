#!/bin/bash

set -e

REGISTRY_URL=docker.io

function check_requirements() {
  if [[ -z "$REGISTRY_USERNAME" ]]; then
    echo "Please provide an environment variable 'REGISTRY_USERNAME' for pushing the image."
    exit 1
  elif [[ -z "$REGISTRY_PASSWORD" ]]; then
    echo "Please provide an environment variable 'REGISTRY_PASSWORD' for pushing the image."
    exit 1
  elif [[ -z "$IMAGE_NAME" ]]; then
    echo "Please provide an environment variable 'IMAGE_NAME' for pushing the image."
    exit 1
  elif [[ -z "$TAG" ]]; then
    echo "Please provide an environment variable 'TAG' for pushing the image."
    exit 1
  fi
}

function main() {
  check_requirements

  echo "$REGISTRY_PASSWORD" | docker login --username "$REGISTRY_USERNAME" --password-stdin
  docker push $REGISTRY_USERNAME/$IMAGE_NAME:$TAG
}

main
