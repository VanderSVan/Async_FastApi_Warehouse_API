from src.utils.auth.password_cryptograph import PasswordCryptographer
from src.api.models.user import UserModel
from src.api.models.product import ProductModel


def prepare_data_for_insertion(users: list, products: list) -> dict:
    """Main function."""
    users: list[dict] = encode_user_passwords(users)
    return {
        UserModel: users,
        ProductModel: products
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
