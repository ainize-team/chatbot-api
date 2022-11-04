import os

from fastapi import APIRouter, Request

from schemas import ServerStatus

from . import v1


router = APIRouter()
router.include_router(v1.router, prefix="/v1")


@router.get("/")
async def get_server_status(request: Request) -> ServerStatus:
    return ServerStatus(number_of_workers=os.getenv("NUMBER_OF_WORKERS", 1))
