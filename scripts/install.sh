#!/bin/bash

set -e

PACK_VERSION=v0.27.0
DBMATE_VERSION=v1.12.1

function check_requirements() {
  if [[ -z "$(command -v curl)" ]]; then
    echo "Please install 'curl' before running this script"
    exit 1
  elif [[ -z "$(command -v python3)" ]]; then
    echo "Please install 'python3' before running this script"
    exit 1
  fi
}

function download_and_install_dbmate() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ `uname -m` == 'arm64' ]]; then
      DBMATE_SOURCE_URL="https://github.com/amacneil/dbmate/releases/download/$DBMATE_VERSION/dbmate-macos-arm64"
    else
      DBMATE_SOURCE_URL="https://github.com/amacneil/dbmate/releases/download/$DBMATE_VERSION/dbmate-macos-amd64"
    fi
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    DBMATE_SOURCE_URL="https://github.com/amacneil/dbmate/releases/download/$DBMATE_VERSION/dbmate-linux-amd64"
  else
    echo "Please install 'pack' using a supported operating system (macos or linux)"
    exit 1
  fi

  (mkdir -p bin || true) && curl -sSL "$DBMATE_SOURCE_URL" > bin/dbmate
  chmod +x ./bin/dbmate
}

function main() {
  check_requirements

  if [[ -z "$(command -v bin/dbmate)" ]]; then
    download_and_install_dbmate
  fi

  if [[ -n "$(command -v asdf)" ]]; then
    asdf install
  fi

  if [[ -z "$(command -v virtualenv)" ]]; then
    pip3 install virtualenv
  fi

  test -d .venv || virtualenv .venv
	. .venv/bin/activate

  pip3 install --upgrade pip

  if [[ "$OSTYPE" == "darwin"* ]]; then
    OPENSSL_LOCATION=$(brew --prefix openssl)
    export LDFLAGS="-I/$OPENSSL_LOCATION/include -L/$OPENSSL_LOCATION/lib"
  fi

  python3 -m pip install --no-cache -r requirements-dev.txt
}

main
