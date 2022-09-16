from src.api.models.user import UserModel
from src.utils.auth.password_cryptograph import PasswordCryptographer


def prepare_data_for_insertion(users: list) -> dict:
    """Main function."""
    users: list[dict] = encode_user_passwords(users)
    return {'users': users}


def encode_user_passwords(users: list[dict]):
    for user in users:
        user_password = user.get('password')

        if user_password:
            hashed_password = PasswordCryptographer.bcrypt(user_password)
            user['hashed_password'] = hashed_password
            del user['password']
        else:
            raise ValueError('user_json should have password field')

    return users
