from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer


class Base(DeclarativeBase):
    pass


class Operations(Base):
    """
        Хранение информации о последней сделке по валюте. Пример:
        currency: 'BTCUSDT' (from url)
        operation: '2L' (from request)
        buy: '0.01' (from mapping)
        initial_sell: '0.002' (from mapping)
        sell: '0.002' (from mapping)
        amount: '0.02' (total amount)
    """
    __tablename__ = "operations"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    currency = Column(String, nullable=False, unique=True)
    operation = Column(String, nullable=False)
    buy = Column(String, nullable=False)
    initial_sell = Column(String, nullable=False)
    sell = Column(String, nullable=False)
    amount = Column(String, nullable=False)


class Profits(Base):
    __tablename__ = "profits"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    currency = Column(String, nullable=False, unique=True)
    operation = Column(String, nullable=False)
