import random

import cv2

from utils.cache_colors import get_color_from_redis, store_color_in_redis


def get_random_contrast_color():
    return random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)


async def generate_bounding_boxes(redis_client, image, boxes):
    for box in boxes:
        x, y, w, h = int(box['x'] - box['width'] / 2), int(box['y'] - box['height'] / 2), int(box['width']), int(
            box['height'])
        confidence = box['confidence']

        label = box['class']
        color = await get_color_from_redis(redis_client, label)
        if color is None:
            color = get_random_contrast_color()
            await store_color_in_redis(redis_client, label, color)

        cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)

        text = f"{label} {int(confidence * 100)}%"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_TRIPLEX, 0.4, 1)
        cv2.rectangle(image, (x, y - text_height - 5), (x + text_width, y), color, -1)
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
