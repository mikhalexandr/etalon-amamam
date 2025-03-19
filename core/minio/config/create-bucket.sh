#!/bin/sh

sleep 3

# Set the Minio alias
mc alias set myminio http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Check if the bucket exists
if mc ls myminio/etalon; then
  echo "Bucket 'etalon' already exists."
else
  # Create the bucket if it doesn't exist
  mc mb myminio/etalon
fi
