from abc import ABC, abstractmethod
from typing import Text


class ShoeId(Text):

    def __init__(self, value: Text):
        self.__value = value

    @property
    def value(self) -> Text:
        return self.__value

    @classmethod
    def create(cls, name: Text) -> "ShoeId":
        return cls(name)


class ShoeName(Text):

    def __init__(self, value: Text):
        self.__value = value

    @property
    def value(self) -> Text:
        return self.__value

    @classmethod
    def create(cls, name: Text) -> "ShoeName":
        return cls(name)


class Shoe:

    def __init__(self, _id: ShoeId, name: ShoeName):
        self.__id = _id
        self.__name = name

    @property
    def id(self) -> ShoeId:
        return self.__id

    @property
    def name(self) -> ShoeName:
        return self.__name


class ShoeRepository(ABC):

    @abstractmethod
    def save(self, shoe: Shoe) -> None:
        pass
