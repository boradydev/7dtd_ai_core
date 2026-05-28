import os
from collections.abc import Callable
from dataclasses import field
from typing import Any


def environ[Type](
    cast_type: Callable[[Any], Type],
    key: str,
) -> Type:
    def _cast_type() -> Type:
        return cast_type(os.environ[key])

    return field(default_factory=_cast_type)


def environ_get[Type](
    cast_type: Callable[[Any], Type],
    key: str,
) -> Type | None:
    def _cast_type() -> Type | None:
        value = os.environ.get(key)
        if value is None:
            return None
        return cast_type(value)

    return field(default_factory=_cast_type)
