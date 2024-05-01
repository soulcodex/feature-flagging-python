from typing import Text, Dict, Tuple

from shared.domain.flag import FlagType, FlagName, FlagValue, Flag, FlagRepository, FlagRetriever as FlagFetcher


class FlagRetriever(FlagFetcher):

    def __init__(self, flags: Dict[Text, Tuple[FlagValue, FlagType]], repository: FlagRepository):
        self.__flags = flags
        self.__repository = repository

    async def flag_by_name(self, name: FlagName) -> Flag:
        self.__guard(name)

        default_value, flag_type = self.__default_value(name)
        value = await self.__repository.search_by_name(name=name, flag_type=flag_type)

        return Flag(name, default_value, value)

    def __guard(self, name: FlagName) -> None:
        if name.lower() not in self.__flags:
            raise KeyError(f"feature flag <{name.lower()}> doesn't exist")

    def __default_value(self, name: FlagName) -> Tuple[FlagValue, FlagType]:
        return self.__flags.get(name.lower())
