#!/bin/bash

set -e

function check_requirements() {
    if [[ -z "$(command -v dbmate)" ]]; then
        echo "Please install 'dbmate' before running the migration script"
        exit 1
    elif [[ -z "$DATABASE_URL" ]]; then
        echo "Please provide a uri for accessing the database."
        exit 1
    fi
}

function main() {
    check_requirements

    dbmate wait

    dbmate \
        --migrations-dir db/migrations \
        --schema-file db/schema.sql \
        up
}

main