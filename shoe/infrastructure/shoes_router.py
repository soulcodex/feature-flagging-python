from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from typing_extensions import Annotated
from ulid import ULID

from shoe.application.create_shoe import CreateShoeHandler, CreateShoeCmd
from shoe.infrastructure.dependency_injection import create_shoe_handler

shoes_router = APIRouter(tags=["Shoes"])


class CreateShoe(BaseModel):
    name: str


@shoes_router.post('', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def create_shoe(shoe: CreateShoe, handler: Annotated[CreateShoeHandler, Depends(create_shoe_handler)]) -> None:
    cmd = CreateShoeCmd(shoe_id=str(ULID()), name=shoe.name)
    await handler.handle(cmd)
