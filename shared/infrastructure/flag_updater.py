from typing import Text, Dict, Tuple, Callable, Any, Union

from shared.domain.flag import FlagType, FlagName, FlagValue, Flag, FlagRepository, FlagUpdater as Updater
from shared.infrastructure.flag_value_serialization import boolean_flag_serializer


class FlagUpdater(Updater):

    def __init__(self, flags: Dict[Text, Tuple[FlagValue, FlagType]], repository: FlagRepository):
        self.__flags = flags
        self.__repository = repository
        self.__flag_serializer: Dict[FlagType, Callable[[Any], Union[bytes, str, int]]] = {
            FlagType.BOOLEAN: boolean_flag_serializer
        }

    async def update(self, name: FlagName, value: FlagValue) -> None:
        self.__guard(name)
        default_value, flag_type = self.__default_value(name)
        flag = Flag(name=name, default_value=default_value, value=value)
        await self.__repository.save(flag=flag, flag_type=flag_type)

    def __guard(self, name: FlagName) -> None:
        if name.lower() not in self.__flags:
            raise KeyError(f"feature flag <{name.lower()}> does not exist")

    def __default_value(self, name: FlagName) -> Tuple[FlagValue, FlagType]:
        return self.__flags.get(name.lower())
