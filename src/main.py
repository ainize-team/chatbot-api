from api import router
from config import app_settings
from fastapi import FastAPI

from enums import EnvEnum
from event_handlers import start_app_handler


def get_app() -> FastAPI:
    fast_api_app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        debug=app_settings.app_env == EnvEnum.DEV,
    )
    fast_api_app.add_event_handler("startup", start_app_handler(fast_api_app))
    fast_api_app.include_router(router)
    return fast_api_app


app = get_app()
