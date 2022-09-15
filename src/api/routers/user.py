from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.models.user import UserModel
from src.api.crud_operations.user import UserOperation
from src.api.swagger.user import (
    UserSwaggerGetAll,
    UserSwaggerGet,
    UserSwaggerDelete,
    UserSwaggerPatch,
    UserSwaggerPost,

    UserOutputGetAll,
    UserOutputGet,
    UserOutputDelete,
    UserOutputPatch,
    UserOutputPost
)
from src.utils.response_generation.main import get_text

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", **asdict(UserOutputGetAll()))
async def get_all_users(user: UserSwaggerGetAll = Depends()
                        ) -> list[UserModel] | list[None]:
    """
    Returns all users from db by parameters.
    Only available to admins.
    """
    crud = UserOperation(user.db)
    return await crud.find_all_by_params(phone=user.phone, status=user.status)


@router.get("/{user_id}", **asdict(UserOutputGet()))
async def get_user(user: UserSwaggerGet = Depends()
                   ) -> UserModel | None:
    """
    Returns one user from db by user id.
    Only available to admins.
    """
    crud = UserOperation(user.db)
    return await crud.find_by_id_or_404(user.user_id)


@router.delete("/{user_id}", **asdict(UserOutputDelete()))
async def delete_user(user: UserSwaggerDelete = Depends()
                      ) -> JSONResponse:
    """
     Deletes user from db by user id.
     Only available to admins.
     """
    crud = UserOperation(user.db)
    await crud.delete_obj(user.user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('delete').format(crud.model_name, user.user_id)
        }
    )


@router.patch("/{user_id}", **asdict(UserOutputPatch()))
async def patch_user(user: UserSwaggerPatch = Depends()
                     ) -> JSONResponse:
    """
    Updates user data.
    Only available to admins.
    """
    crud = UserOperation(user.db)
    await crud.patch_obj(user.user_id, user.data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('patch').format(crud.model_name, user.user_id)
        }
    )


@router.post("/create/", **asdict(UserOutputPost()))
async def add_user(user: UserSwaggerPost = Depends()
                   ) -> JSONResponse:
    """
    Adds new user into db.
    Only available to admins.
    """
    crud = UserOperation(user.db)
    await crud.add_obj(user.data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": get_text('post').format(crud.model_name)
        }
    )
