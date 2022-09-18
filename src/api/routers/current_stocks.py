from dataclasses import asdict

from fastapi import APIRouter, Depends


from src.api.swagger.current_stocks import (
    CurrentStocksInterfaceGetAll,
    CurrentStocksOutputGetAll
)
from src.api.crud_operations.current_stocks import get_current_stocks

router = APIRouter(
    prefix="/current_stocks",
    tags=["current stocks"],
)


@router.get("/", **asdict(CurrentStocksOutputGetAll()))
async def get_all_current_stocks(current_stocks: CurrentStocksInterfaceGetAll = Depends()
                                 ):
    """
    Returns all current stocks from db by parameters.
    Only available to admins.
    """

    return await get_current_stocks(current_stocks.db,
                                    datetime=current_stocks.datetime,
                                    warehouse_id=current_stocks.warehouse_id)
