
from ..components.custom import spacer

import reflex as rx

def loading_page():
    return rx.center(
        spacer(height='40px'),
        rx.chakra.spinner(),
        height='20em',
        width='100%'
    )
