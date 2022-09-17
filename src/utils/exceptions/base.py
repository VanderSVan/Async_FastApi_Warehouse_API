from dataclasses import dataclass
from typing import NoReturn, Any

from fastapi import status

from src.utils.color_logging.main import logger
from src.utils.response_generation.main import get_text


@dataclass
class JSONException(Exception):
    status_code: int
    message: str
    headers: dict | None = None


class CRUDException:
    @staticmethod
    def raise_error_500(text_err: str = None) -> NoReturn:
        if text_err:
            logger.exception(text_err)

        raise JSONException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=get_text('err_500')
        )

    @staticmethod
    def raise_duplicate_err(model_name) -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=get_text('duplicate').format(model_name)
        )

    @staticmethod
    def raise_obj_not_found(model_name, id_) -> NoReturn:
        """
        If there is no object with the given id in the db, then raises the error.
        """
        raise JSONException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=get_text('not_found').format(model_name, id_)
        )

    @staticmethod
    def raise_param_not_found(model_name: str, param_name: str, param_value: Any) -> NoReturn:
        """
        If there is no object with the given parameter in the db, then raises the error.
        """
        raise JSONException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=get_text('param_not_found').format(model_name,
                                                       param_name,
                                                       param_value)
        )

    @staticmethod
    def raise_no_patch_data() -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=get_text('err_patch_no_data')
        )
