from typing import Text

from shared.domain.flag import FlagRetriever, FlagName
from shoe.domain.shoe import ShoeRepository, Shoe, ShoeId, ShoeName


class ShoeCreator:

    def __init__(self, current: ShoeRepository, new: ShoeRepository, ff_retriever: FlagRetriever):
        self.__current_persistence = current
        self.__new_persistence = new
        self.__ff_retriever = ff_retriever

    async def create(self, _id: Text, name: Text) -> None:
        shoe_id, shoe_name = ShoeId.create(_id), ShoeName.create(name)
        shoe = Shoe(_id=shoe_id, name=shoe_name)
        new_shoe_persistence_is_activated = await self.new_persistence_is_activated()
        if new_shoe_persistence_is_activated:
            await self.__new_persistence.save(shoe)
            return
        await self.__current_persistence.save(shoe)

    async def new_persistence_is_activated(self) -> bool:
        flag_name = FlagName.create("new_shoes_persistence_activated")
        flag = await self.__ff_retriever.flag_by_name(name=flag_name)
        return True if flag.default_value_if_none() else False
