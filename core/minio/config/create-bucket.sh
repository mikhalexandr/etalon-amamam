#!/bin/sh

sleep 3

# Установка MinIO alias
mc alias set myminio http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Проверка существования Bucket
if mc ls myminio/etalon; then
  echo "Bucket 'etalon' already exists."
else
  # Создание Bucket
  mc mb myminio/etalon
fi
