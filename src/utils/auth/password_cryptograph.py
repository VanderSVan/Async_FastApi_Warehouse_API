from passlib.context import CryptContext
from passlib.exc import UnknownHashError

PASSWORD_CONTEXT = CryptContext(schemes='bcrypt', deprecated="auto")


class PasswordCryptographer:
    """Encrypts and decrypts password"""

    @classmethod
    def bcrypt(cls, password: str) -> str:
        """
        Encrypts password.
        :param password: User password.
        :return: Encrypted password as string.
        """

        return PASSWORD_CONTEXT.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Decrypts and checks the user’s password;
        :param plain_password: The password entered by the user;
        :param hashed_password: User password from the db.
        :return: bool
        """
        try:
            result = PASSWORD_CONTEXT.verify(
                plain_password,
                hashed_password,
            )
        except UnknownHashError:
            result = False
        return result


if __name__ == '__main__':
    # Demonstration of work:
    input_password: str = 'simple_password'
    hashed: str = PasswordCryptographer.bcrypt(input_password)
    verified: bool = PasswordCryptographer.verify(input_password, hashed)
    print(f"{input_password=}\n"
          f"{hashed=}\n"
          f"length={len(hashed)}\n"
          f"Is the password a match: {verified}")

