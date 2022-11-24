from fastapi import APIRouter

from fastapi_template.app.api.controller import user_controller, file_controller

api_router = APIRouter()
api_router.include_router(user_controller.router, prefix="/user")
api_router.include_router(file_controller.router, prefix="/file")
