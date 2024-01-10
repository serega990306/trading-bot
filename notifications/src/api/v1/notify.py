import logging
from http import HTTPStatus
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from services.notify_handler import NotifyHandler
from db.session import get_session

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    '/{currency}',
    summary='Получение нотификаций'
)
async def post_notification(
        currency: str,
        request: Request,
        # data: str,
        session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        logger.info('Получено оповещение {}'.format(currency))
        data = await request.body()
        data = data.decode()
        logger.info(data)
        handler = NotifyHandler(currency, data, session)
        await handler.handle()
        return {'status': HTTPStatus.OK}
    except Exception as e:
        logger.error('Ошибка обработки оповещения {}:'.format(currency))
        logger.error('{}\n{}'.format(type(e), e))
        return {'status': HTTPStatus.INTERNAL_SERVER_ERROR}

