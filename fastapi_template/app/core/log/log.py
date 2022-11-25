import logging
from typing import Any

import structlog
from asgi_correlation_id import correlation_id
from orjson import orjson


def add_correlation(
        logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add request id to log message."""
    if request_id := correlation_id.get():
        event_dict["request_id"] = request_id
    return event_dict


def dumps(*a, **kw) -> str:
    try:
        # This raises "dumps() got unexpected keyword argument"
        return orjson.dumps(*a, **kw).decode()

        # This works:
        # return orjson.dumps(*a, default=kw.get("default")).decode()

    except Exception as e:
        return f"Opps {e} ### {a} ### {kw}"


structlog.configure(
    processors=[
        add_correlation,
        # This performs the initial filtering, so we don't
        # evaluate e.g. DEBUG when unnecessary
        structlog.stdlib.filter_by_level,
        # Adds logger=module_name (e.g __main__)
        structlog.stdlib.add_logger_name,
        # Adds level=info, debug, etc.
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        # Performs the % string interpolation as expected
        structlog.stdlib.PositionalArgumentsFormatter(),
        # Include the stack when stack_info=True
        structlog.processors.StackInfoRenderer(),
        # Include the exception when exc_info=True
        # e.g log.exception() or log.warning(exc_info=True)'s behavior
        structlog.processors.format_exc_info,
        # Decodes the unicode values in any kv pairs
        structlog.processors.UnicodeDecoder(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.processors.JSONRenderer(serializer=dumps),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True
)
logger = structlog.get_logger()
