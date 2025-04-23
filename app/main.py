import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount(
    settings.MEDIA_URL,
    StaticFiles(directory=settings.MEDIA_ROOT),
    name='media',
)

app.include_router(api_router, prefix='/api')
