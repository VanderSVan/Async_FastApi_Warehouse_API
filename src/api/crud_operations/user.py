from sqlalchemy import select, insert, and_, asc

from src.api.crud_operations.base_crud_operations import ModelOperation
from src.api.crud_operations.utils.base_crud_utils import QueryExecutor
from src.api.models.user import UserModel
from src.api.schemas.user.base_schemas import UserPostSchema
from src.utils.auth.password_cryptograph import PasswordCryptographer


class UserOperation(ModelOperation):
    def __init__(self, db):
        self.model = UserModel
        self.model_name = 'user'
        self.db = db

    async def find_all_by_params(self, **kwargs) -> list[UserModel]:
        phone = kwargs.get('phone')
        status = kwargs.get('status')
        query = (
            select(self.model)
            .where(and_(
                        (UserModel.phone == phone
                         if phone is not None else True),
                        (UserModel.status == status
                         if status is not None else True),
                       )
                   )
            .order_by(asc(self.model.id)))
        return await QueryExecutor.get_multiple_result(query, self.db)

    async def add_obj(self, new_user_schema: UserPostSchema) -> bool:
        max_id: int = await self.get_max_id()
        hashed_password = PasswordCryptographer.bcrypt(new_user_schema.password)

        new_user_data: dict = dict(
            id=max_id + 1,
            hashed_password=hashed_password,
            status='unconfirmed',
            **new_user_schema.dict(exclude={'password'})
        )
        query = insert(self.model).values(new_user_data)
        return await QueryExecutor.add_obj(query, self.db, self.model_name)
