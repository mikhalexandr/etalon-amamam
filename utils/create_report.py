import io
import os

import cv2

from core.minio.access import get_minio
from core.redis.access import get_redis
from core.roboflow.access import get_roboflow
from core.settings import settings
from utils.generate_bounding_boxes import generate_bounding_boxes
from utils.generate_txt_file import generate_txt_report


async def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


async def create_report(folder, image_url, reports_count):
    roboflow_client = await get_roboflow()
    redis_client = await get_redis()
    minio_client = await get_minio()

    image = cv2.imread(image_url)
    image = await resize_image(image, 1000, 1000)

    result = await roboflow_client.infer_async(image, model_id=settings.roboflow_model_id)

    filename_txt = await generate_txt_report(folder, reports_count, result)
    with open(filename_txt, 'r', encoding='utf-8') as text_file:
        text_data = text_file.read()
    text_data_bytes = io.BytesIO(text_data.encode('utf-8'))
    minio_client.put_object(
        bucket_name=settings.minio_bucket,
        object_name=f"{folder}/{os.path.basename(filename_txt)}",
        data=text_data_bytes,
        length=len(text_data_bytes.getvalue()),
        content_type='text/plain'
    )
    print(result)
    filename_png = None
    if 'predictions' in result:
        filename_png = await generate_bounding_boxes(redis_client, image, reports_count, result['predictions'])
        with open(filename_png, 'rb') as image_file:
            image_data = image_file.read()
        image_data_bytes = io.BytesIO(image_data)
        minio_client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=f"{folder}/{os.path.basename(filename_png)}",
            data=image_data_bytes,
            length=len(image_data),
            content_type='image/png'
        )
    else:
        with open(image_url, 'rb') as image_file:
            image_data = image_file.read()
        minio_client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=f"{folder}/{os.path.basename(f'./assets/report_{reports_count}.png')}",
            data=image_data,
            length=len(image_data),
            content_type='image/png'
        )

    return filename_txt, filename_png
