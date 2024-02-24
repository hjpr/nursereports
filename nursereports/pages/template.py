
from ..components.c2a import c2a
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.custom import spacer

import reflex as rx

def template() -> rx.Component:
    return rx.flex(

        c2a(),

        navbar(),
        
        # CONTENT CONTAINER
        rx.flex(
            # STYLING FOR CONTENT CONTAINER
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
        ),

        footer(),

        # STYLING FOR BODY CONTAINER
        flex_direction='column',
        align_items='center',
        min_height='100vh'

    )
