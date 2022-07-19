from fastapi import APIRouter

from services.api.endpoint.fashiondetect import yolox_router
from services.api.endpoint.test import test_router

main_router = APIRouter(prefix="/v1")

main_router.include_router(yolox_router)
main_router.include_router(test_router)