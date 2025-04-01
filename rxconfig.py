
import os
import reflex as rx

from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv("api_url")
api_key = os.getenv("api_key")
jwt_secret = os.getenv("jwt_secret")

config = rx.Config(
    app_name="nursereports",
    api_url='http://localhost:8000',
    tailwind={},
    show_built_with_reflex=False,
    suplex={
        "api_url": api_url,
        "api_key": api_key,
        "jwt_secret": jwt_secret,
        "let_jwt_expire": False,
    }
)