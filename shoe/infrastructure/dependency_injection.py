import redis.asyncio as redis
from fastapi import Depends
from typing_extensions import Annotated

from shared.domain.flag import FlagRetriever
from shared.infrastructure.dependency_injection import redis_client
from shared.infrastructure.flag_dependency_injection import flag_retriever
from shoe.application.create_shoe import CreateShoeHandler
from shoe.domain.shoe_creator import ShoeCreator
from shoe.infrastructure.in_memory_shoe_repository import InMemoryShoeRepository
from shoe.infrastructure.redis_shoe_repository import RedisShoeRepository


def redis_shoe_repository(client: Annotated[redis.Redis, Depends(redis_client)]) -> RedisShoeRepository:
    return RedisShoeRepository(client=client)


def in_memory_shoe_repository() -> InMemoryShoeRepository:
    return InMemoryShoeRepository()


def shoe_creator(
        current_persistence: Annotated[InMemoryShoeRepository, Depends(in_memory_shoe_repository)],
        new_persistence: Annotated[RedisShoeRepository, Depends(redis_shoe_repository)],
        ff_retriever: Annotated[FlagRetriever, Depends(flag_retriever)],
) -> ShoeCreator:
    return ShoeCreator(current=current_persistence, new=new_persistence, ff_retriever=ff_retriever)


def create_shoe_handler(creator: Annotated[ShoeCreator, Depends(shoe_creator)]) -> CreateShoeHandler:
    return CreateShoeHandler(creator=creator)
