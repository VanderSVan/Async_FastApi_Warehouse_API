from datetime import datetime as dt

from src.utils.auth.password_cryptograph import PasswordCryptographer
from src.api.models.user import UserModel
from src.api.models.product import ProductModel
from src.api.models.warehouse_group import WarehouseGroupModel
from src.api.models.warehouse import WarehouseModel
from src.api.models.price import PriceModel


def prepare_data_for_insertion(users: list,
                               products: list,
                               warehouse_groups: list,
                               warehouses: list,
                               prices: list
                               ) -> dict:
    """Main function."""
    users: list[dict] = encode_user_passwords(users)
    prices: list[dict] = process_dt_objects(prices)
    return {
        UserModel: users,
        ProductModel: products,
        WarehouseGroupModel: warehouse_groups,
        WarehouseModel: warehouses,
        PriceModel: prices
    }


def encode_user_passwords(users: list[dict]):
    for user in users:
        user_password = user.get('password')
        user_hashed_password = user.get('hashed_password')

        if user_password:
            hashed_password = PasswordCryptographer.bcrypt(user_password)
            user['hashed_password'] = hashed_password
            del user['password']

        elif user_hashed_password:
            pass

        else:
            raise ValueError('user_json should have password field')

    return users


def process_dt_objects(data: list[dict]) -> list[dict]:
    return [process_single_dt_objects(obj) for obj in data]


def process_single_dt_objects(obj_dt: dict) -> dict:
    obj_dt['datetime'] = dt.strptime(obj_dt['datetime'], '%Y-%m-%dT%H:%M:%S')
    return obj_dt
