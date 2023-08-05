import logging
from functools import wraps
from inspect import signature
from typing import Any, Callable, ParamSpec, TypeVar

from prungo.constants import LOG_CALL_LIMIT, SENTINEL, SERVICE_NAME
from prungo.interfaces import logger_type
from prungo.utils import DisplayStyle, dynamic_fstring, introspect_params, safe_cast

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(SERVICE_NAME)


def make_decorator(method: Callable[[Callable, Any], Any]):
    """
    decorator that converts a function to a decorator;
    the function to become a decorator must accept a method as its first argument
    it should also accept *args and **kwargs as is standard
    """

    @wraps(method)
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs):
            return method(func, *args, **kwargs)

        return inner

    return decorator


def log_call(
    method: Callable | None = None,
    *,
    log: logger_type = logging.getLogger(SERVICE_NAME),
    static: Any = None,
    param_name: Any = None,
    log_length: int = LOG_CALL_LIMIT,
    separator: str = "|",
    filler: str = "-",
):
    """
    :method: function being passed to `log_call` unless other params are being used
    :log: optional logger - uses default if left blank
    :static: a static value to be logged
    :param_name: the parameter name to be logged
    """

    @make_decorator
    def decorator(func: Callable, *args, **kwargs):
        logs = []
        logs.append(func.__name__)

        if static is not None:
            logs.append(safe_cast(static, str, SENTINEL))

        if param_name is not None:
            logs.append(introspect_params(param_name, args, kwargs, func))

        logs = list(filter(lambda x: x is not SENTINEL, logs))

        sep = f" {separator.strip()} "
        log_text = f" {sep.join(logs).strip()} "
        log.info(dynamic_fstring(log_text, filler, DisplayStyle.CENTRE, log_length))
        return func(*args, **kwargs)

    return decorator if method is None else decorator(method)
