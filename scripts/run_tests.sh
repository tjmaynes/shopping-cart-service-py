#!/bin/bash

set -e

if [[ -z $DATABASE_URI ]]; then
    echo "Please provide a uri for accessing the database."
    exit 1
elif [[ -z $DATABASE_MIGRATIONS_DIR ]]; then
    echo "Please provide a migrations directory."
    exit 1
elif [[ -z $DATABASE_SCHEMA_FILE ]]; then
    echo "Please provide a scheme file location."
    exit 1
elif [[ -z $FLASK_APP ]]; then
    echo "Please provide an entrypoint to the api service."
    exit 1
fi

# Wait for database
DATABASE_URL=$DATABASE_URI dbmate wait

# Run migrations
DATABASE_URL=$DATABASE_URI dbmate \
--migrations-dir $DATABASE_MIGRATIONS_DIR \
--schema-file $DATABASE_SCHEMA_FILE \
up

python cart_api/api_test.py