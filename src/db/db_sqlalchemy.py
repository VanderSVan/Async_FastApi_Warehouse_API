from sys import modules

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

settings = get_settings()

if "pytest" in modules:
    URL = settings.get_test_database_url()
else:
    URL = settings.get_database_url()

async_engine = create_async_engine(URL, future=True, echo=True)

async_session = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=async_engine)

BaseModel = declarative_base()
