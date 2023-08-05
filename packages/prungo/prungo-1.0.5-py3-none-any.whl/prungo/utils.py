from enum import Enum
from inspect import signature
from math import ceil, floor
from typing import Any, Callable

from prungo.constants import SENTINEL


def iter_get(
    iter: list | tuple,
    index: int,
    default=None,
) -> Any | None:
    if index < len(iter):
        return iter[index]

    return default


def safe_cast(
    value: Any,
    cast_type: type,
    default: Any = None,
):
    try:
        return cast_type(value)
    except TypeError:
        pass

    if default is None:
        return value

    return default


def introspect_params(key: str, args: tuple, kwargs: dict, func: Callable):
    param = kwargs.get(key, SENTINEL)
    if param is not SENTINEL:
        return param

    sig = signature(func)

    for index, sig_key in enumerate(sig.parameters.keys()):
        if key == sig_key:
            return iter_get(iter=args, index=index, default=SENTINEL)

    return SENTINEL


class DisplayStyle(Enum):
    LEFT = "left"
    CENTRE = "centre"
    RIGHT = "right"


def repeat_chars(text: str, limit: int):
    count = limit // len(text)
    extra_chars = limit - (count * len(text))
    return f"{text * count}{text[:extra_chars]}"


def dynamic_fstring(
    text: str,
    wrapping_char: str,
    style: DisplayStyle,
    limit: int,
) -> str:
    chars_to_add = limit - len(text)

    if chars_to_add <= 0:
        return text

    wrapping = repeat_chars(wrapping_char, chars_to_add)

    if style == DisplayStyle.CENTRE:
        half = chars_to_add // 2
        return f"{wrapping[:half]}{text}{wrapping[half:]}"

    match style:
        case DisplayStyle.LEFT:
            return f"{text}{wrapping}"
        case DisplayStyle.RIGHT:
            return f"{wrapping}{text}"
