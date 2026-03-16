import json

from redis.asyncio import Redis


class StreamWriter:
    def __init__(self, redis: Redis, stream_name: str) -> None:
        self.redis = redis
        self.stream_name = stream_name

    async def write(self, payload: dict) -> str:
        return await self.redis.xadd(self.stream_name, {"data": json.dumps(payload)})
