import logging
from http import HTTPStatus
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from services.notify_handler import NotifyHandler
from db.session import get_session

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/{currency}",
    summary="Получение нотификаций",
    openapi_extra={"x-request-id": "request ID"}
)
async def post_notification(
        currency: str,
        request: Request,
        session: AsyncSession = Depends(get_session)
) -> dict:
    logger.info(f'Получено оповещение')
    data = await request.body()
    data = data.decode()
    logger.info(data)
    handler = NotifyHandler(currency, data, session)
    handler.handle()
    return {'status': HTTPStatus.OK}
