async def store_color_in_redis(redis_client, _id, color):
    color_str = ','.join(map(str, color))
    await redis_client.set(_id, color_str)


async def get_color_from_redis(redis_client, _id):
    color_str = await redis_client.get(_id)
    if color_str:
        return tuple(map(int, color_str.decode('utf-8').split(',')))
    return None
