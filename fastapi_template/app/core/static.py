import logging
from pathlib import Path
from typing import NoReturn

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from fastapi_template.config import settings


def mount_static(app: FastAPI) -> NoReturn:
    """Mount the static at defined uploaded file if it exists.
    Parameters:
        app: the app to mount the static to.
    """
    static_folder = settings.FILE_UPLOAD_FOLDER or str(Path.home())
    try:
        app.mount(f"{settings.FILE_URL_PREFIX}", StaticFiles(directory=static_folder))
        logging.debug('Mounted static')
    except RuntimeError:
        logging.warning(f'no folder at {static_folder} to serve at /static')
