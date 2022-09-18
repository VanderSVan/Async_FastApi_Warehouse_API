from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from src.api.models.price import PriceModel
from src.api.swagger.price import (
    PriceInterfaceGetAll,
    PriceInterfaceGet,
    PriceInterfaceDelete,
    PriceInterfacePatch,
    PriceInterfacePost,

    PriceOutputGetAll,
    PriceOutputGet,
    PriceOutputDelete,
    PriceOutputPatch,
    PriceOutputPost
)
from src.api.crud_operations.price import PriceOperation
from src.utils.response_generation.main import get_text

router = APIRouter(
    prefix="/prices",
    tags=["prices"],
)


@router.get("/", **asdict(PriceOutputGetAll()))
async def get_all_prices(price: PriceInterfaceGetAll = Depends()
                         ) -> list[PriceModel] | list[None]:
    """
    Returns all prices from db by parameters.
    Only available to admins.
    """
    crud = PriceOperation(price.db)
    return await crud.find_all_by_params(price=price.price,
                                         from_dt=price.from_dt,
                                         to_dt=price.to_dt,
                                         product_id=price.product_id,
                                         warehouse_group_id=price.warehouse_group_id,
                                         offset=price.offset,
                                         limit=price.limit)


@router.get("/{price_id}", **asdict(PriceOutputGet()))
async def get_price(price: PriceInterfaceGet = Depends()
                    ) -> PriceModel | None:
    """
    Returns one price from db by price id.
    Only available to admins.
    """
    crud = PriceOperation(price.db)
    return await crud.find_by_id(price.price_id)


@router.delete("/{price_id}", **asdict(PriceOutputDelete()))
async def delete_price(price: PriceInterfaceDelete = Depends()) -> ORJSONResponse:
    """
    Deletes price from db by price id.
    Only available to admins.
    """
    crud = PriceOperation(price.db)
    await crud.delete_obj(price.price_id)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('delete').format(crud.model_name, price.price_id)
        }
    )


@router.patch("/{price_id}", **asdict(PriceOutputPatch()))
async def patch_price(price: PriceInterfacePatch = Depends()
                      ) -> ORJSONResponse:
    """
    Updates price data.
    Only available to admins.
    """
    crud = PriceOperation(price.db)
    await crud.patch_obj(price.data, price.price_id)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('patch').format(crud.model_name, price.price_id)
        }
    )


@router.post("/create", **asdict(PriceOutputPost()))
async def add_price(price: PriceInterfacePost = Depends()) -> ORJSONResponse:
    """
    Adds new price into db.
    Only available to admins.
    """
    crud = PriceOperation(price.db)
    await crud.add_obj(price.data)

    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": get_text('post').format(crud.model_name)
        }
    )
