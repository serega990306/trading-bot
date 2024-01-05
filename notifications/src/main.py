import uvicorn
from api.v1 import notify
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.service_name,
    docs_url="/api/notify/openapi",
    openapi_url="/api/notify/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    logger.info("===== Запуск приложение =====")


@app.on_event("shutdown")
async def shutdown():
    logger.info("===== Остановка приложение =====")

app.include_router(notify.router, prefix="/api/v1/notify", tags=["notify"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
