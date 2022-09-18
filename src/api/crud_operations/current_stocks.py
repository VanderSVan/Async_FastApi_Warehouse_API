from datetime import datetime as dt

from sqlalchemy import select, and_, desc, func, asc, tuple_

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.product import ProductModel
from src.api.models.price import PriceModel
from src.api.models.product_count import ProductCountModel


async def get_current_stocks(session: AsyncSession, **kwargs):
    warehouse_id: int = kwargs.get('warehouse_id')
    datetime: dt = kwargs.get('datetime')
    processed_dt: dt = datetime if datetime else dt.utcnow()

    # Sorry for this KOLKHOZ.
    # If I had more time I would change this shit.
    # To do this, I need to change the structure a little.
    ##########################################

    # Subquery to get the maximum datetime from the price table.
    max_price_dt = (
        select(PriceModel.product_id, func.max(PriceModel.datetime))
        .where(PriceModel.datetime <= processed_dt,
               PriceModel.warehouse_id == warehouse_id)
        .group_by(PriceModel.product_id)
        .subquery()
    )
    # Subquery to get filtered price IDs.
    last_price_dt_subquery = (
        select(PriceModel.id)
        .where(and_(PriceModel.warehouse_id == warehouse_id,
                    tuple_(PriceModel.product_id, PriceModel.datetime).in_(max_price_dt)))
        .order_by(desc(PriceModel.datetime))
        .subquery()

    )
    # Subquery to get the maximum datetime from the product count table.
    max_count_dt = (
        select(ProductCountModel.product_id, func.max(ProductCountModel.datetime))
        .where(ProductCountModel.datetime <= processed_dt,
               ProductCountModel.warehouse_id == warehouse_id)
        .group_by(ProductCountModel.product_id)
        .subquery()
                        )

    # Subquery to get filtered product count IDs.
    last_count_dt_subquery = (
        select(ProductCountModel.id)
        .where(and_(ProductCountModel.warehouse_id == warehouse_id,
                    tuple_(ProductCountModel.product_id, ProductCountModel.datetime).in_(max_count_dt)))
        .order_by(desc(ProductCountModel.datetime))
        .subquery()
    )
    # Main query.
    select_query = (select(ProductModel.id.label('product_id'),
                           ProductModel.name.label('product_name'),
                           PriceModel.warehouse_id,
                           PriceModel.price,
                           PriceModel.datetime.label('dt_price'),
                           ProductCountModel.count,
                           ProductCountModel.datetime.label('dt_count')
                           )
                    .join(ProductCountModel, ProductModel.id == ProductCountModel.product_id)
                    .join(PriceModel, ProductModel.id == PriceModel.product_id)
                    .where(and_(PriceModel.id.in_(last_price_dt_subquery),
                                ProductCountModel.id.in_(last_count_dt_subquery)))
                    .order_by(asc(ProductModel.id))
                    )
    query = await session.execute(select_query)
    return query.fetchall()

