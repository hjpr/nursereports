
import os
import reflex as rx

from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="nursereports",
    api_url='http://localhost:8000',
    tailwind={},
    show_built_with_reflex=False,
    suplex={
        "api_url": os.getenv("api_url"),
        "api_key": os.getenv("api_key"),
        "jwt_secret": os.getenv("jwt_secret"),
        "service_role": os.getenv("service_role"),
        "let_jwt_expire": False,
    },
    groq_key=os.getenv("GROQ_KEY"),
    mailgun_url=os.getenv("MAILGUN_URL"),
    mailgun_api_key=os.getenv("MAILGUN_API_KEY"),
)