from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey

from src.db.db_sqlalchemy import BaseModel


class PriceModel(BaseModel):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(scale=2))
    datetime = Column(DateTime)

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
