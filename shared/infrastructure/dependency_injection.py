import redis.asyncio as redis


async def redis_client() -> redis.Redis:
    client = await redis.from_url("redis://localhost:6379")
    await client.ping()
    yield client
    await client.aclose()
