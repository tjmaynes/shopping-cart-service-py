#!/bin/bash

set -e

PACK_VERSION=v0.21.1
DBMATE_VERSION=v1.12.1

function check_requirements() {
  if [[ -z "$(command -v curl)" ]]; then
    echo "Please install 'curl' before running this script"
    exit 1
  elif [[ -z "$(command -v python)" ]]; then
    echo "Please install 'python' before running this script"
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

function download_and_install_pack() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ `uname -m` == 'arm64' ]]; then
      PACK_SOURCE_URL="https://github.com/buildpacks/pack/releases/download/$PACK_VERSION/pack-$PACK_VERSION-macos-arm64.tgz"
    else
      PACK_SOURCE_URL="https://github.com/buildpacks/pack/releases/download/$PACK_VERSION/pack-$PACK_VERSION-macos.tgz"
    fi
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PACK_SOURCE_URL="https://github.com/buildpacks/pack/releases/download/$PACK_VERSION/pack-$PACK_VERSION-linux.tgz"
  else
    echo "Please install 'pack' using a supported operating system (macos or linux)"
    exit 1
  fi

  if [[ ! -f "bin/pack-$PACK_VERSION.tgz" ]]; then
    (mkdir -p bin || true) && curl -sSL "$PACK_SOURCE_URL" > bin/pack-$PACK_VERSION.tgz
  fi

  tar -xzf bin/pack-$PACK_VERSION.tgz -C bin
  rm -rf bin/pack-$PACK_VERSION*
}

function download_and_install_openssl() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ -z "$(command -v brew)" ]]; then
      echo "Please install 'homebrew' to install openssl."
      exit 1
    fi
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    DBMATE_SOURCE_URL="https://github.com/amacneil/dbmate/releases/download/$DBMATE_VERSION/dbmate-linux-amd64"
  else
    echo "Please install 'pack' using a supported operating system (macos or linux)"
    exit 1
  fi
}

function main() {
  check_requirements

  if [[ -z "$(command -v bin/pack)" ]]; then
    download_and_install_pack
  fi

  if [[ -z "$(command -v bin/dbmate)" ]]; then
    download_and_install_dbmate
  fi

  if [[ -z "$(command -v virtualenv)" ]]; then
    pip3 install virtualenv
  fi

  test -d .venv || virtualenv .venv
	. .venv/bin/activate

  pip3 install --upgrade pip

  if [[ "$OSTYPE" == "darwin"* ]]; then
    LDFLAGS="-I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib" \
    python3 -m pip install --no-cache -r requirements-dev.txt
  fi
}

main
