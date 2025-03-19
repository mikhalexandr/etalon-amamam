from aiobotocore.session import get_session

from core.settings import settings


async def get_minio_client():
    session = get_session()
    return session.create_client(
        's3',
        endpoint_url=settings.minio_url,
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        aws_session_token=None,
        region_name='us-east-1',
        verify=None,
        use_ssl=settings.minio_secure
    )
