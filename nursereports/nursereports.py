
from .client.pages import *
# from .tests.pages import *

import reflex as rx



app = rx.App(
    theme=rx.theme(
        scaling="90%"
    ),
    stylesheets=[
        "https://cdn.jsdelivr.net/npm/@fontsource-variable/inter/index.css",
        "https://cdn.jsdelivr.net/npm/@fontsource/geist-mono/index.css",
        "stylesheet.css",
    ],
)