from typing import Any, Optional

from sqlalchemy.sql.type_api import TypeEngine
from strong_typing.core import JsonType

from .conversion_common import Converter, JsonTypeCast, get_type_cast


def create_value_converter(value_type: TypeEngine) -> Converter:
    type_cast: Optional[JsonTypeCast] = get_type_cast(type(value_type))

    if type_cast is None:
        return lambda value: value
    else:
        cast = type_cast  # hint to type checker

        def _convert_value(value: JsonType) -> Optional[Any]:
            if value is None:
                return None
            return cast(value)

        return _convert_value
