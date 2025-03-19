from typing import Dict
import numpy

import cv2

from core.settings import settings
from utils.generate_bounding_boxes import generate_bounding_boxes_for_construction, generate_bounding_boxes_for_safety


async def resize_photo(image, max_width, max_height):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


async def process_photo(
        num: int,
        object_id: str,
        file: bytes,
        reports_count: int,
        minio_client,
        redis_client,
        roboflow_client
) -> Dict[float, int, int, dict, int, int, int, int, int, dict]:

    image = numpy.frombuffer(file, numpy.uint8)
    image = await resize_photo(image, 1000, 1000)
    image_2 = image.copy()

    result_construction = await roboflow_client.infer_async(image, model_id=settings.roboflow_model_ids[0])

    time = result_construction.get("time")
    predictions = result_construction.get("predictions", [])
    prediction_amount = len(predictions)
    types_amount = max(predictions, key=lambda x: x.get('class_id')).get('class')

    if "predictions" in result_construction:
        await generate_bounding_boxes_for_construction(redis_client, image, result_construction['predictions'])

    _, buffer = cv2.imencode('.png', image)
    image_bytes = buffer.tobytes()

    object_name = f"{object_id}/{reports_count}/construction/{num}.png"
    async with minio_client:
        await minio_client.put_object(
            Bucket=settings.minio_bucket,
            Key=object_name,
            Body=image_bytes
        )

    result_safety_1 = await roboflow_client.infer_async(image_2, model_id=settings.roboflow_model_ids[2])
    result_safety_2 = await roboflow_client.infer_async(image_2, model_id=settings.roboflow_model_ids[1])

    boxes1 = result_safety_1.get("boxes", [])
    boxes2 = result_safety_2.get("boxes", [])
    combined_boxes = boxes1 + boxes2
    safety_labels = {"No-Hardhat", "No-mask", "No-safetyvest"}
    count_person_violations = 0
    count_construction_violations = 0
    count_person_with_helmet = 0
    count_person_without_helmet = 0
    filtered_boxes = []
    for box in combined_boxes:
        label = box["label"]
        if label == "Person" or label == "Sky":
            continue
        filtered_boxes.append(box)
        if label in safety_labels:
            count_person_violations += 1
        elif label == "Invalid_balcony":
            count_construction_violations += 1
        elif label == "person_with_helmet":
            count_person_with_helmet += 1
        elif label == "person_without_helmet":
            count_person_without_helmet += 1
    count_person = count_person_without_helmet + count_person_with_helmet

    if "boxes" in filtered_boxes:
        await generate_bounding_boxes_for_safety(redis_client, image_2, filtered_boxes['boxes'])

    _, buffer = cv2.imencode('.png', image_2)
    image_bytes = buffer.tobytes()

    object_name = f"{object_id}/{reports_count}/safety/{num}.png"
    async with minio_client:
        await minio_client.put_object(
            Bucket=settings.minio_bucket,
            Key=object_name,
            Body=image_bytes
        )

    return {
        "time": time,
        "prediction_amount": prediction_amount,
        "types_amount": types_amount,
        "predictions": predictions,
        "count_person_violations": count_person_violations,
        "count_construction_violations": count_construction_violations,
        "count_person_with_helmet": count_person_with_helmet,
        "count_person_without_helmet": count_person_without_helmet,
        "count_person": count_person,
        "filtered_boxes": filtered_boxes
    }
