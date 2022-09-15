from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

setting = get_settings()

URL = setting.get_database_url()
engine = create_async_engine(URL, future=True, echo=True)

async_session = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=engine)

BaseModel = declarative_base()
