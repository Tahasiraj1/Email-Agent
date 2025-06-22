from redis.asyncio import Redis
from dataclasses import dataclass
from typing import List

@dataclass
class RedisCollector:
    redis = Redis()
    key: str = "email_agent_logs"

    async def collect(self, message: str) -> None:
        await self.redis.rpush(self.key, message)

    async def get_messages(self) -> List[str]:
        messages = await self.redis.lrange(self.key, 0, -1)
        return [msg.decode('utf-8') for msg in messages]
    
    async def clear(self):
        await self.redis.delete(self.key)
    
