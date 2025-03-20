from typing import List, Dict

from core.minio.access import get_minio_client


# Получение списка файлов в MinIO
async def list_files_in_bucket(bucket_name: str, prefix: str, minio_client) -> List[str]:
    paginator = minio_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    files = []
    async for page in page_iterator:
        for obj in page.get('Contents', []):
            files.append(obj['Key'])
    return files


# Генерация списка файлов в MinIO
async def generate_files_dict(bucket_name: str, base_prefix: str) -> Dict[str, List[str]]:
    files_dict = {}

    minio_client = await get_minio_client()
    async with minio_client as client:
        base_files = await list_files_in_bucket(bucket_name, base_prefix, client)
        subfolders = {file.split('/')[2] for file in base_files if file.startswith(base_prefix) and file.count('/') > 1}
        for subfolder in subfolders:
            prefix = f"{base_prefix}{subfolder}/"
            files = await list_files_in_bucket(bucket_name, prefix, client)
            files_dict[subfolder] = [f"{file}" for file in files]

    return files_dict
