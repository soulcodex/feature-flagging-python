from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette import status
from typing import Text, Any, Union, Dict
from typing_extensions import Annotated

from shared.domain.flag import FlagUpdater, FlagRetriever, FlagName, FlagValue, Flag as FeatureFlag
from shared.infrastructure.flag_dependency_injection import flag_retriever, flag_updater


class FlagView(BaseModel):
    name: str
    default_value: Any
    value: Any


class FlagUpdate(BaseModel):
    value: Union[bool, Dict[Text, Any]] = Field(union_mode="left_to_right")


flags_router = APIRouter(tags=["Flags"])


@flags_router.get(
    "/{flag_name}",
    name="Retrieve a feature flag",
    description="Retrieve the current feature flag value",
    response_model=FlagView,
    status_code=status.HTTP_200_OK
)
async def feature_flag_by_name(
        flag_name: Text,
        retriever: Annotated[FlagRetriever, Depends(flag_retriever)]
):
    try:
        flag: FeatureFlag = await retriever.flag_by_name(name=FlagName.create(flag_name))
        print(flag)
        return FlagView(
            name=flag.name.lower(),
            default_value=flag.default.value,
            value=flag.value.value if flag.value is not None else None
        )
    except KeyError as e:
        return JSONResponse(content={'error': e.__str__()}, status_code=status.HTTP_404_NOT_FOUND)


@flags_router.patch(
    "/{flag_name}",
    name="Update a feature flag value",
    description="Update a feature flag value in runtime",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_feature_flag_by_name(
        flag_name: Text,
        flag_update: FlagUpdate,
        updater: Annotated[FlagUpdater, Depends(flag_updater)]
):
    try:
        await updater.update(name=FlagName.create(flag_name), value=FlagValue(flag_update.value))
    except KeyError as e:
        return JSONResponse(content={'error': e.__str__()}, status_code=status.HTTP_404_NOT_FOUND)
