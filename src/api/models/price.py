from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey

from src.db.db_sqlalchemy import BaseModel


class PriceModel(BaseModel):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    price = Column(Float(precision=2))
    datetime = Column(DateTime, unique=True)

    product_id = Column(
        Integer, ForeignKey('products.id',
                            onupdate='CASCADE',
                            ondelete='CASCADE')
    )
    warehouse_group_id = Column(
        Integer, ForeignKey('warehouse_groups.id',
                            onupdate='CASCADE',
                            ondelete='CASCADE')
    )
