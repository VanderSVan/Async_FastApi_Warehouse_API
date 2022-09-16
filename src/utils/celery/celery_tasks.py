import asyncio
from typing import Literal

from src.config import get_settings
from src.utils.celery.celery_config import app
from src.utils.composing_email.main import compose_email_with_action_link

settings = get_settings()


@app.task(bind=True)
def send_email(self,
               username: str,
               email: str,
               action: Literal['confirm_email'] | Literal['reset_password']
               ):
    """
    Sends an email to the user using celery.
    """
    try:
        email, params = compose_email_with_action_link(
            username=username,
            email=email,
            action=action,
        )
        print(f"\n\n\n{email=}, {params=}")
        message, template_name = params
        asyncio.run(email.send_message(message=message, template_name=template_name))

    except Exception as err:
        raise self.retry(exc=err, countdown=60)

    return True
