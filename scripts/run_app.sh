#!/bin/bash

set -e

if [[ -z $DATABASE_URI ]]; then
  echo "Please provide a uri for accessing the database."
  exit 1
elif [[ -z $FLASK_APP ]]; then
  echo "Please provide an entrypoint to the api service."
  exit 1
fi


echo "Attempt to run database migrations..."

DATABASE_URL=$DATABASE_URI dbmate wait
DATABASE_URL=$DATABASE_URI dbmate \
  --migrations-dir cart_database/migrations \
  --schema-file cart_database/schema.sql \
  up


echo "Run shopping_cart_service..."
DATABASE_URI=$DATABASE_URI \
  FLASK_APP=$FLASK_APP \
  shopping_cart_service
