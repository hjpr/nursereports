
from ..components.c2a import c2a
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.custom import spacer

import reflex as rx

def template() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        flex_direction='column',
        align_items='center',
        min_height='100vh'
    )

def content() -> rx.Component:
    return rx.flex(
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
    )