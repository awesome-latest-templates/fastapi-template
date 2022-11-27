"""Contain helpers to customize logging for the service."""
import json
import logging
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from pprint import pformat
from typing import TypedDict

from asgi_correlation_id import correlation_id
from gunicorn.glogging import Logger
from loguru import logger

from fastapi_template.config import settings

try:
    from orjson import dumps
except Exception as ex:
    from json import dumps


# References
# Solution comes from:
#   https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
#   https://github.com/pahntanapat/Unified-FastAPI-Gunicorn-Log
#   https://github.com/Delgan/loguru/issues/365
#   https://loguru.readthedocs.io/en/stable/api/logger.html#sink


def set_log_extras(record: TypedDict):
    """set_log_extras [summary].
    [extended_summary]
    Args:
        record ([type]): [description]
    """
    # Log datetime in UTC time zone, even if server is using another timezone
    record["extra"]["datetime"] = datetime.now(timezone.utc)
    record["extra"]["host"] = os.getenv("HOSTNAME", os.getenv("COMPUTERNAME", platform.node())).split(".")[0]
    record["extra"]["pid"] = os.getpid()
    record["extra"]["request_id"] = correlation_id.get() or 'App'
    record["extra"]["app_name"] = settings.PROJECT_NAME


#
# Set Gunicorn loggin handler to NullHandler, this allow
# Loguru to capture the logs emitted by Gunicorn
#
class StubbedGunicornLogger(Logger):
    """StubbedGunicornLogger [summary].
    [extended_summary]
    Args:
        Logger ([type]): [description]
    """

    def setup(self, cfg):
        """Make the setup of Gunicorn Logger.
        [extended_summary]
        Args:
            cfg ([type]): [description]
        """
        self.loglevel = self.LOG_LEVELS.get(cfg.loglevel.lower(), logging.INFO)

        handler = logging.NullHandler()

        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)

        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)

        self.error_logger.setLevel(self.loglevel)
        self.access_logger.setLevel(self.loglevel)


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        """Emit [summary].
        [extended_summary]
        Args:
            record ([type]): [description]
        """
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        # Find caller from where originated the logging call
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: TypedDict) -> str:
    """Return a custom format for loguru loggers.
    Uses pformat for log any data like request/response body
    >>> [   {   'count': 2,
    >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    format_string = "<green>{extra[datetime]}</green> | "
    # format_string += "<green>{extra[app_name]}</green> | "
    # format_string += "<green>{extra[host]}</green> | "
    # format_string += "<green>{extra[pid]}</green> | "
    format_string += "<green>{extra[request_id]}</green> | "
    format_string += "<level>{level}</level> | "
    format_string += "<cyan>{name}</cyan>:"
    format_string += "<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    format_string += "<level>{message}</level>"

    # This is to nice print data, like:
    # logger.bind(payload=dataobject).info("Received data")
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"

    return format_string


def orjson_log_sink(msg):
    """orjson_log_sink [summary].
    [extended_summary]
    Args:
        msg ([type]): [description]
    """
    r = msg.record
    rec = {
        "elapsed": r["elapsed"].total_seconds(),
        "time": r["time"].isoformat(),
        "level": {
            "name": r["level"].name,
            "no": r["level"].no,
        },
        "process": {"id": r["process"].id, "name": r["process"].name},
        "thread": {"id": r["thread"].id, "name": r["thread"].name},
        "file": r["file"].path,
    }

    if r["exception"]:
        rec["exception"] = str(msg)

    for k, v in r.items():
        print(k, type(v), v)
        if k in rec:
            continue
        rec[k] = v

    print(dumps(rec), flush=True)


class CustomizeLogger:

    @classmethod
    def make_logger(cls, config_path: Path = Path(__file__).with_name("logging_config.json")):
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')
        logging_path = Path(logging_config.get('path') or str(Path.home()), logging_config.get('filename'))
        logger = cls.customize_logging(
            filepath=logging_path,
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            json=False
        )
        return logger

    @classmethod
    def load_logging_config(cls, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

    @classmethod
    def customize_logging(
            cls,
            filepath: Path,
            level: str,
            rotation: str,
            retention: str,
            json: bool = True
    ):
        """Define the logger to be used by the service based on loguru.

        Parameters:
            filepath: the path where to store the logfiles.
            level: the minimum log-level to log.
            rotation: when to rotate the logfile.
            retention: when to remove logfiles.

        Returns:
            the logger to be used by the service.
            :param json:

        """
        filepath.parent.mkdir(parents=True, exist_ok=True)

        logger.remove()
        intercept_handler = InterceptHandler()
        seen = set()
        for name in [
            *logging.root.manager.loggerDict.keys(),
            "gunicorn",
            "gunicorn.access",
            "gunicorn.error",
            "uvicorn",
            "uvicorn.access",
            "uvicorn.error",
            "uvicorn.config",
            'fastapi',
            'sqlalchemy'
        ]:
            if name not in seen:
                seen.add(name.split(".")[0])
                logging.getLogger(name).handlers = [intercept_handler]

        logger.add(
            sys.stdout,
            colorize=True,
            # Asynchronous, Thread-safe, Multiprocess-safe
            enqueue=True,
            backtrace=True,
            diagnose=True,
            level=level.upper(),
            format=format_record
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format_record
        )
        if json:
            logger.configure(handlers=[
                {
                    "sink": orjson_log_sink,
                    "colorize": True,
                    "serialize": json,
                    "diagnose": True,
                    "backtrace": True,
                }
            ])
        else:
            logger.configure(
                handlers=[
                    {
                        "sink": sys.stdout,
                        "colorize": True,
                        # https://loguru.readthedocs.io/en/stable/api/logger.html#sink
                        # "sink": "./somefile.log",
                        # "rotation": "10 MB",
                        "enqueue": True,
                        "backtrace": True,
                        "diagnose": True,
                        "serialize": False,
                        "level": level.upper(),
                        "format": format_record
                    },
                    {
                        "sink": str(filepath),
                        "rotation": rotation,
                        "retention": retention,
                        "enqueue": True,
                        "backtrace": True,
                        "diagnose": True,
                        "serialize": False,
                        "level": level.upper(),
                        "format": format_record
                    }
                ]
            )

        logging.basicConfig(handlers=[intercept_handler], level=0)
        logger.configure(patcher=set_log_extras)

        return logger
