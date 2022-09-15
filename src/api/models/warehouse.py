from sqlalchemy import Column, Integer, String, ForeignKey

from src.db.db_sqlalchemy import BaseModel


class WarehouseModel(BaseModel):
    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), unique=True)

    warehouse_group_id = Column(
        Integer, ForeignKey('warehouse_groups.id',
                            onupdate='CASCADE',
                            ondelete='CASCADE')
    )
