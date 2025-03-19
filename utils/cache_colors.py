async def store_color_in_redis(redis_client, class_id, color):
    color_str = ','.join(map(str, color))
    await redis_client.set(class_id, color_str)


async def get_color_from_redis(redis_client, class_id):
    color_str = await redis_client.get(class_id)
    if color_str:
        return tuple(map(int, color_str.decode('utf-8').split(',')))
    return None
