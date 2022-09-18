from sqlalchemy import Column, Integer, DateTime, ForeignKey

from src.db.db_sqlalchemy import BaseModel


class ProductCountModel(BaseModel):
    __tablename__ = 'product_counts'

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
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
