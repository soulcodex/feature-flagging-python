from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Optional, Text, Any


class FlagType(IntEnum):
    BOOLEAN = 1
    LIST = 2


class FlagName(Text):

    @classmethod
    def create(cls, value: Text) -> "FlagName":
        return FlagName(value.lower())


class FlagValue:

    def __init__(self, value: Any):
        self.__value = value

    @property
    def value(self) -> Any:
        return self.__value


class Flag:

    def __init__(self, name: FlagName, default_value: FlagValue, value: Optional[FlagValue] = None):
        self.__name = name
        self.__default_value = default_value
        self.__value = value

    @property
    def name(self) -> FlagName:
        return self.__name

    @property
    def default(self) -> FlagValue:
        return self.__default_value

    @property
    def value(self) -> Optional[FlagValue]:
        return self.__value

    def default_value_if_none(self) -> Any:
        if self.__value is not None:
            return self.__value.value
        return self.__default_value.value


class FlagRepository(ABC):

    @abstractmethod
    def save(self, flag: Flag, flag_type: FlagType) -> None:
        pass

    @abstractmethod
    def search_by_name(self, name: FlagName, flag_type: FlagType) -> Optional[FlagValue]:
        pass


class FlagRetriever(ABC):

    @abstractmethod
    def flag_by_name(self, name: FlagName) -> Flag:
        pass


class FlagUpdater(ABC):

    @abstractmethod
    def update(self, name: FlagName, value: FlagValue) -> None:
        pass
