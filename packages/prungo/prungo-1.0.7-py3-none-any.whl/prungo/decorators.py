import logging
from functools import wraps
from inspect import signature
from typing import Any, Callable, ParamSpec, TypeVar

from prungo.constants import (
    CALLED_STR,
    FAILED_STR,
    LOG_CALL_LIMIT,
    SENTINEL,
    SERVICE_NAME,
    SUCCESS_STR,
)
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
    success: bool = False,
    separator: str = "|",
    filler: str = "-",
):
    """
    :method: function being passed to `log_call` unless other params are being used
    :log: optional logger - uses default if left blank
    :static: a static value to be logged
    :param_name: the parameter name to be logged
    :log_length: maximum length of the decorations added to the log message
    :success: log twice, on call and success/failure; provides context
    :separator: separate segments by this character
    :filler: add this character repeated to the outside of the message
    """

    @make_decorator
    def decorator(func: Callable, *args, **kwargs):
        logs = []
        logs.append(func.__name__)
        sep = f" {separator.strip()} "

        def execute_log():
            clean_logs = list(filter(lambda x: x is not SENTINEL, logs))
            log_text = f" {sep.join(clean_logs).strip()} "
            display_log = dynamic_fstring(
                text=log_text,
                wrapping_char=filler,
                style=DisplayStyle.CENTRE,
                limit=log_length,
            )
            log.info(display_log)

        def check_success(
            param: Any,
            success_str: str = SUCCESS_STR,
            fail_str: str = FAILED_STR,
        ):
            if not param:
                return fail_str

            return success_str

        if static is not None:
            logs.append(safe_cast(static, str, SENTINEL))

        if param_name is not None:
            logs.append(introspect_params(param_name, args, kwargs, func))

        if success:
            logs.append(CALLED_STR)

        execute_log()
        response = func(*args, **kwargs)

        if success:
            logs.pop(-1)
            logs.append(check_success(response))
            execute_log()

        return response

    return decorator if method is None else decorator(method)
