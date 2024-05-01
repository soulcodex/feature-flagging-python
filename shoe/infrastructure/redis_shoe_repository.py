from typing import Text, Dict, Any

import redis.asyncio as redis

import shoe.domain.shoe as shoes_domain


class RedisShoeRepository(shoes_domain.ShoeRepository):

    def __init__(self, client: redis.Redis):
        self.__client = client

    async def save(self, shoe: shoes_domain.Shoe) -> None:
        await self.__client.hset(name=self.__key(shoe.id), mapping=self.__serialize(shoe))

    @staticmethod
    def __key(_id: shoes_domain.ShoeId) -> Text:
        return f'shoes::{_id.value}'

    @staticmethod
    def __serialize(shoe: shoes_domain.Shoe) -> Dict[Text, Any]:
        return {'id': shoe.id.value, 'name': shoe.name.value}
