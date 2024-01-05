from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# class Notification(BaseModel):
#     x_request_id: str | None = None
#     notice_id: UUID
#     users_id: List[UUID]
#     template_id: UUID | None
#     transport: str
#     priority: int | None = 0
#     msg_type: str | None = None
#     expire_at: datetime


@router.post(
    "/{currency}",
    summary="Получение нотификаций",
    openapi_extra={"x-request-id": "request ID"}
)
async def post_notification(
        currency: str,
        request: Request
) -> dict:
    logger.info(f'Получено оповещение')
    data = await request.body()
    data = data.decode()
    logger.info(data)
    return {'status': HTTPStatus.OK}
