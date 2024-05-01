from typing import Text, Optional, Dict

from redis.asyncio import Redis

from shared.domain.flag import FlagRepository, Flag, FlagName, FlagValue, FlagType
from shared.infrastructure.flag_value_serialization import (
    boolean_flag_deserializer,
    boolean_flag_serializer,
    FlagSerializer,
    FlagDeserializer
)


class RedisFlagRepository(FlagRepository):

    def __init__(self, client: Redis):
        self.client = client
        self.__flag_value_deserializer: Dict[FlagType, FlagDeserializer] = {
            FlagType.BOOLEAN: boolean_flag_deserializer
        }
        self.__flag_serializer: Dict[FlagType, Callable[[Any], FlagSerializer]] = {
            FlagType.BOOLEAN: boolean_flag_serializer
        }

    async def save(self, flag: Flag, flag_type: FlagType) -> None:
        flag_value_serializer = self.__flag_serializer.get(flag_type)
        flag_value = flag.value
        if flag_value is None or flag_value_serializer is None:
            return

        serialized_value = flag_value_serializer(flag_value.value)
        await self.client.set(name=self.__key(flag.name), value=serialized_value)

    async def search_by_name(self, name: FlagName, flag_type: FlagType) -> Optional[FlagValue]:
        current_flag_value, value = None, await self.client.get(name=self.__key(name.lower()))
        flag_value_deserializer = self.__flag_value_deserializer.get(flag_type, None)
        if value is not None and flag_value_deserializer is not None:
            current_flag_value = flag_value_deserializer(value.decode("utf-8"))

        return current_flag_value

    @staticmethod
    def __key(name: FlagName) -> Text:
        return f'feature_flag::{name}'
