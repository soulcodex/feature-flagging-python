import redis.asyncio as redis
from UnleashClient import UnleashClient
from fastapi import Depends
from typing_extensions import Annotated

from shared.domain.flag import FlagType, FlagValue, FlagUpdater as Updater, FlagRepository, FlagRetriever as Fetcher
from shared.infrastructure.dependency_injection import redis_client
from shared.infrastructure.flag_retriever import FlagRetriever
from shared.infrastructure.flag_updater import FlagUpdater
from shared.infrastructure.redis_flag_repository import RedisFlagRepository
from shared.infrastructure.unleash_flag_repository import UnleashFlagRepository


async def redis_flag_repository(client: Annotated[redis.Redis, Depends(redis_client)]) -> RedisFlagRepository:
    return RedisFlagRepository(client=client)


async def unleash_flag_repository() -> UnleashFlagRepository:
    token = "feature-flagging-v1-tech-talk:development.335156dc13ce3346b99f67c7ef6afc50c21e6614b4e8996c0d9b18da"
    client = UnleashClient(
        url="https://app.unleash-hosted.com/demo/api/",
        app_name="feature-flagging-v1-tech-talk",
        custom_headers={'Authorization': token})

    return UnleashFlagRepository(client=client)


async def feature_flag_repository(repository: Annotated[FlagRepository, Depends(redis_flag_repository)]) -> FlagRepository:
    return repository


async def flag_retriever(repository: Annotated[FlagRepository, Depends(feature_flag_repository)]) -> Fetcher:
    return FlagRetriever(
        flags={
            'new_shoes_persistence_activated': (FlagValue(False), FlagType.BOOLEAN)
        },
        repository=repository
    )


async def flag_updater(repository: Annotated[FlagRepository, Depends(feature_flag_repository)]) -> Updater:
    return FlagUpdater(
        flags={
            'new_shoes_persistence_activated': (FlagValue(False), FlagType.BOOLEAN)
        },
        repository=repository
    )
