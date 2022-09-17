from sqlalchemy import Column, Integer, String

from src.db.db_sqlalchemy import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=100), unique=True, index=True)
    hashed_password = Column(String(length=100))
    email = Column(String(length=100), unique=True, index=True)
    phone = Column(String(length=15), unique=True, index=True)
    role = Column(String(length=100))
    status = Column(String(length=25))
