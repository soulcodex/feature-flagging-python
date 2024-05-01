from typing import Optional

from UnleashClient import UnleashClient

from shared.domain.flag import FlagRepository, Flag, FlagName, FlagValue, FlagType


class UnleashFlagRepository(FlagRepository):

    def __init__(self, client: UnleashClient):
        self.__client = client
        self.__client.initialize_client()

    async def save(self, flag: Flag, flag_type: FlagType) -> None:
        pass

    async def search_by_name(self, name: FlagName, flag_type: FlagType) -> Optional[FlagValue]:
        value = self.__client.is_enabled(feature_name=name.lower())
        return FlagValue(value=value)
