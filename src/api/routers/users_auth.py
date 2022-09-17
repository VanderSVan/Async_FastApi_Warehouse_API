from datetime import timedelta as td
from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from src.config import get_settings
from src.api.models.user import UserModel
from src.api.swagger.user_auth import (
    UserAuthSwaggerGetUser,
    UserAuthSwaggerCreateToken,
    UserAuthSwaggerRegisterUser,
    UserAuthSwaggerConfirmEmail,
    UserAuthSwaggerResetPassword,
    UserAuthSwaggerConfirmResetPassword,

    UserAuthOutputGetCurrentUser,
    UserAuthOutputConfirmEmail,
    UserAuthOutputResetPassword,
    UserAuthOutputGetToken,
    UserAuthOutputRegister,
    UserAuthOutputConfirmNewPassword
)
from src.api.crud_operations.user_auth import UserAuthOperation
from src.utils.response_generation.main import get_text
from src.utils.auth.signature import Signer
from src.utils.auth.jwt import JWT

settings = get_settings()

router = APIRouter(
    prefix=f"{settings.users_auth_router}",
    tags=["users auth"],
)


@router.get('/me', **asdict(UserAuthOutputGetCurrentUser()))
def get_current_user(user: UserAuthSwaggerGetUser = Depends()
                     ) -> UserModel:
    """Returns current user data."""
    return user.current_confirmed_user


@router.post("/token", **asdict(UserAuthOutputGetToken()))
async def create_token(user: UserAuthSwaggerCreateToken = Depends()
                       ) -> dict:
    """
    Gets authenticated data and returns a token if the data is valid;
    :param user: contain input data such as login and password.
    :return: {'access_token': str, 'token_type': 'bearer'}
    """
    crud = UserAuthOperation(user.db)
    user = await crud.authenticate_user(user.form_data.username, user.form_data.password)
    access_token_expires = td(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", **asdict(UserAuthOutputRegister()))
async def register_user(user: UserAuthSwaggerRegisterUser = Depends()
                        ) -> ORJSONResponse:
    """
    Gets new user data and saves it into db.
    It then sends an email to the user to confirm the password;
    :param user: user data.
    :return: UserModel.
    """
    crud = UserAuthOperation(user.db)

    await crud.add_obj(user.data)
    crud.send_user_registration_email(user.data)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": get_text('registration_email')}
    )


@router.get('/confirm-email/{sign}/', **asdict(UserAuthOutputConfirmEmail()))
async def confirm_email(user: UserAuthSwaggerConfirmEmail = Depends()
                        ) -> ORJSONResponse:
    """
    Request to confirm the user’s email;
    """
    decoded_user_data: dict = Signer.unsign_object(obj=user.sign)
    username: str = decoded_user_data.get('username')

    crud = UserAuthOperation(user.db)
    await crud.confirm_user_email(username)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": get_text('email_confirmed')}
    )


@router.get('/reset-password', **asdict(UserAuthOutputResetPassword()))
async def reset_password(user: UserAuthSwaggerResetPassword = Depends()
                         ) -> ORJSONResponse:
    """
    Request to reset the user’s password.
    The user must be in authenticated status else he cannot access this endpoint.
    It then sends an email to the user to reset the password;
    """
    crud = UserAuthOperation(user.db)

    await crud.find_by_id_or_404(user.current_confirmed_user.id)
    crud.send_password_reset_email(user.current_confirmed_user)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": get_text('reset_password')}
    )


@router.post('/confirm-reset-password/{sign}/',
             **asdict(UserAuthOutputConfirmNewPassword())
             )
async def confirm_reset_password(user: UserAuthSwaggerConfirmResetPassword = Depends()):
    """
    Gets the user's new password and saves it in the database.
    """
    decoded_user_data: dict = Signer.unsign_object(obj=user.sign)
    username: str = decoded_user_data.get('username')
    crud = UserAuthOperation(user.db)
    await crud.confirm_reset_password(username, user.new_password_data.password)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": get_text('changed_password')}
    )
