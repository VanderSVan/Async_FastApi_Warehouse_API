from datetime import timedelta as td
from typing import Optional

from blake2signer import Blake2SerializerSigner, errors
from fastapi import status

from src.config import get_settings
from src.utils.exceptions.base import JSONException
from src.utils.response_generation.main import get_text

settings = get_settings()
signer = Blake2SerializerSigner(secret=settings.SECRET_KEY,
                                max_age=td(hours=int(settings.URL_EXPIRE_HOURS)))


class Signer:
    """
    Encodes an object into a digital signature.
    Required to send emails.
    """

    @staticmethod
    def sign_object(obj: dict) -> str:
        """
        Encodes object with signature.
        :param obj: Dictionary.
        :return: Encoded dictionary as string.
        """
        signed = signer.dumps(obj)
        return signed

    @staticmethod
    def unsign_object(obj: str) -> Optional[dict[str]]:
        """
        Decodes object with signature.
        :param obj: Signature as string.
        :return: Decoded signature as string.
        """

        try:
            unsigned = signer.loads(obj)
        except errors.SignedDataError as err:
            raise JSONException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=get_text('decode_signature_fail').format(str(err))
            )
        return unsigned


if __name__ == '__main__':
    # Demonstration of work:
    input_data: dict = {'username': 'some_username'}
    encoded_data: str = Signer.sign_object(input_data)
    decoded_data: dict = Signer.unsign_object(encoded_data)
    print(f"{input_data=}\n"
          f"{encoded_data=}\n"
          f"length={len(encoded_data)}\n"
          f"{decoded_data=}")
