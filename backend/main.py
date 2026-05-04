from fastapi import FastAPI
from app.core.config import settings
from app.api import health
from app.api import identify


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug
)

app.include_router(health.router)
app.include_router(identify.router)

