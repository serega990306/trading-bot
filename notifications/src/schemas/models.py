from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String


class Base(DeclarativeBase):
    pass


class Operations(Base):
    __tablename__ = "operations"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    currency = Column(String, nullable=False, unique=True)
    operation = Column(String, nullable=False)


class Profits(Base):
    __tablename__ = "profits"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    currency = Column(String, nullable=False, unique=True)
    operation = Column(String, nullable=False)
