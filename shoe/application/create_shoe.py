from dataclasses import dataclass

from shoe.domain.shoe_creator import ShoeCreator


@dataclass(frozen=True)
class CreateShoeCmd:
    shoe_id: str
    name: str


class CreateShoeHandler:

    def __init__(self, creator: ShoeCreator):
        self.__creator = creator

    async def handle(self, cmd: CreateShoeCmd) -> None:
        await self.__creator.create(_id=cmd.shoe_id, name=cmd.name)
