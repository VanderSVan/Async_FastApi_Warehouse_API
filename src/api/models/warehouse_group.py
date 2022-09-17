from sqlalchemy import Column, Integer, String

from src.db.db_sqlalchemy import BaseModel


class WarehouseGroupModel(BaseModel):
    __tablename__ = 'warehouse_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), unique=True)


