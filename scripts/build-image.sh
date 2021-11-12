#!/bin/bash

set -e

function check_requirements() {
  if [[ -z "$(command -v bin/pack)" ]]; then
    echo "Please install 'pack' before running this script"
    exit 1
  elif [[ -z "$REGISTRY_USERNAME" ]]; then
    echo "Please provide an environment variable 'REGISTRY_USERNAME' for debugging the image."
    exit 1
  elif [[ -z "$IMAGE_NAME" ]]; then
    echo "Please provide an environment variable 'IMAGE_NAME' for debugging the image."
    exit 1
  elif [[ -z "$TAG" ]]; then
    echo "Please provide an environment variable 'TAG' for debugging the image."
    exit 1
  fi
}

function main() {
  check_requirements

  bin/pack build "$REGISTRY_USERNAME/$IMAGE_NAME:$TAG" \
    --builder paketobuildpacks/builder:base \
    --buildpack gcr.io/paketo-buildpacks/python \
    --buildpack gcr.io/paketo-buildpacks/procfile \
    --default-process web
}

main
