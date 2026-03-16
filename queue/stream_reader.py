import json

from redis.asyncio import Redis


class StreamReader:
    def __init__(self, redis: Redis, stream_name: str, group_name: str, consumer_name: str) -> None:
        self.redis = redis
        self.stream_name = stream_name
        self.group_name = group_name
        self.consumer_name = consumer_name

    async def ensure_group(self) -> None:
        try:
            await self.redis.xgroup_create(self.stream_name, self.group_name, id="0", mkstream=True)
        except Exception as exc:
            if "BUSYGROUP" not in str(exc):
                raise

    async def read(self, count: int = 50, block_ms: int = 2000) -> list[tuple[str, dict]]:
        rows = await self.redis.xreadgroup(groupname=self.group_name, consumername=self.consumer_name, streams={self.stream_name: ">"}, count=count, block=block_ms)
        decoded: list[tuple[str, dict]] = []
        for _, messages in rows:
            for message_id, fields in messages:
                payload = json.loads(fields.get("data", "{}"))
                decoded.append((message_id, payload))
        return decoded

    async def ack(self, message_id: str) -> None:
        await self.redis.xack(self.stream_name, self.group_name, message_id)
