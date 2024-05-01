import json
from typing import Union, Callable, Any

from shared.domain.flag import FlagValue

FlagDeserializer = Callable[[Any], FlagValue]
FlagSerializer = Callable[[Any], Union[bytes, str, int]]


def boolean_flag_deserializer(value: Any) -> FlagValue:
    if value in ['1', '0', 'True', 'False', 1, 0]:
        return FlagValue(bool(json.loads(value.lower())))
    raise ValueError(f'unable to deserialize {value} as <bool>')


def boolean_flag_serializer(value: Any) -> Union[bytes, str, int]:
    if value in [True, False]:
        return int(value)
    raise ValueError(f'unable to serialize {value} as <bool>')
