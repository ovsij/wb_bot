from datetime import datetime
import os
from secrets import token_hex
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship



engine = create_async_engine(f"postgresql+asyncpg://postgres:{os.getenv('PG_PASS')}@{os.getenv('PG_HOST')}:5432/wb_bot")

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"

    id = Column(Integer)
    tg_id = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    was_registered = Column(datetime, default=datetime.now())
    last_use = Column(datetime, default=datetime.now())
    is_admin = Column(Boolean, default=False)
    refer = relationship("User", back_populates='referals')
    referals = relationship("User", back_populates='refer')
    balance = Column(float, default=0)
    logs = relationship("Log", back_populates='user')
    export_token = Column(String, default=token_hex(15))


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    user = relationship("User", back_populates='log')
    action = Column(String)
    datetime = Column(datetime, default=datetime.now())
    