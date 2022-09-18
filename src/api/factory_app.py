from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import ProgrammingError

from src.api.routers import (user,
                             users_auth,
                             product,
                             warehouse_group,
                             warehouse,
                             price,
                             product_count,
                             current_stocks)

from src.utils.exceptions.base import JSONException
from src.utils.color_logging.main import logger
from src.config import get_settings

setting = get_settings()
api_url = setting.API_URL


def create_app(with_logger: bool = True):

    application = FastAPI(title='Warehouse-API',
                          version='0.1.0',
                          docs_url=f'{api_url}/docs',
                          redoc_url=f'{api_url}/redoc',
                          openapi_url=f'{api_url}/openapi.json')

    # Routers
    application.include_router(users_auth.router, prefix=api_url)
    application.include_router(user.router, prefix=api_url)
    application.include_router(product.router, prefix=api_url)
    application.include_router(warehouse_group.router, prefix=api_url)
    application.include_router(warehouse.router, prefix=api_url)
    application.include_router(price.router, prefix=api_url)
    application.include_router(product_count.router, prefix=api_url)
    application.include_router(current_stocks.router, prefix=api_url)

    # Exception handlers
    @application.exception_handler(JSONException)
    async def error_handler_400(request: Request, exception: JSONException):
        logger.exception(exception) if with_logger else None
        return JSONResponse(status_code=exception.status_code,
                            content={"message": exception.message})

    @application.exception_handler(ProgrammingError)
    async def handler_alchemy_integrity_error(request: Request, programming_err):
        logger.exception(programming_err) if with_logger else None
        err_name = "sqlalchemy.exc.ProgrammingError"
        traceback = programming_err.args[0] or str(programming_err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": {'err_name': err_name,
                                                 'traceback': traceback}})

    @application.exception_handler(AttributeError)
    async def handler_alchemy_integrity_error(request: Request, attribute_err):
        logger.exception(attribute_err) if with_logger else None
        err_name = "AttributeError"
        traceback = attribute_err.args or str(attribute_err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": {'err_name': err_name,
                                                 'traceback': traceback}})

    return application
