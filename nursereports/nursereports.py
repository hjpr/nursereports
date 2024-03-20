
from .client.pages import *
# from .tests.pages import *


from .server.middleware.middleware import LoggingMiddleware

import reflex as rx

app = rx.App(
    middleware=[LoggingMiddleware()],
    theme=rx.theme(
        accent_color='teal',
        appearance='light'
    )
)