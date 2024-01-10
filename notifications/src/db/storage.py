import logging
from functools import wraps
from typing import Optional
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.future import select
from sqlalchemy import delete, update

from schemas.models import Operations, Profits

logger = logging.getLogger(__name__)


def error_handler(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            res = await func(self, *args, **kwargs)
            await self.session.commit()
            return res
        except Exception as e:
            logging.error(f'Ошибка взаимодействия с БД:\n{type(e)}\n{e}')
            await self.session.rollback()

    return wrapper


class Storage:

    def __init__(self, session) -> None:
        self.session = session

    @error_handler
    async def check_operation(self, currency) -> Optional[Operations]:
        query = select(Operations).where(Operations.currency == currency)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return row

    @error_handler
    async def add_operation(self, currency, operation, buy, sell, amount):
        query = delete(Operations).where(Operations.currency == currency)
        await self.session.execute(query)
        operation = Operations(currency=currency, operation=operation, buy=buy, sell=sell, amount=amount)
        self.session.add(operation)

    @error_handler
    async def delete_operation(self, currency):
        query = delete(Operations).where(Operations.currency == currency)
        await self.session.execute(query)
