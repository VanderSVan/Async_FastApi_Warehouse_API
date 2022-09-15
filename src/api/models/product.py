from sqlalchemy import Column, Integer, String

from src.db.db_sqlalchemy import BaseModel


class ProductModel(BaseModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), unique=True)
