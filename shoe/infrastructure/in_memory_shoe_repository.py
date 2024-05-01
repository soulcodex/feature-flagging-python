from typing import Dict

import shoe.domain.shoe as shoes_domain


class InMemoryShoeRepository(shoes_domain.ShoeRepository):

    def __init__(self):
        self.__shoes: Dict[shoes_domain.ShoeId, shoes_domain.Shoe] = {}

    async def save(self, shoe: shoes_domain.Shoe) -> None:
        self.__shoes[shoe.id] = shoe
