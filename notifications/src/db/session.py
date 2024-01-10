import asyncio
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import settings
from schemas.models import Base

logger = logging.getLogger(__name__)
engine = create_async_engine(f'sqlite+aiosqlite:////TradingBot.sqlite', echo=settings.echo, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def async_main() -> None:
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)

            # async with async_session() as session:
            #     async with session.begin():
            #         session.query(PositionQuantity).delete()
            #         session.add_all(
            #             [
            #                 PositionQuantity(currency=currency, qty=qty) for currency, qty in mapping.items()
            #             ]
            #         )
            #         await session.commit()
        except Exception as e:
            logging.error(f"Ошибка создания таблиц БД:\n{type(e)}\n{e}")

asyncio.run(async_main())


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
