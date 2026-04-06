from loguru import logger

import httpx
import reflex as rx
import rich

_config = rx.config.get_config()

def mailgun_send_email(sender: str, recipient: str | list, subject: str, text: str) -> None:
    auth = ("api", _config.mailgun_api_key)

    data = {
        "from": sender,
        "to": recipient,
        "subject": subject,
        "text": text
    }

    response = httpx.post(_config.mailgun_url, auth=auth, data=data)
    if response.is_success:
        logger.debug(f"{sender} sent email to {recipient} successfully.")
    else:
        rich.inspect(response)
        logger.critical(f"{sender} failed to send email to {recipient} successfully.")
        raise Exception("Email API error.")
