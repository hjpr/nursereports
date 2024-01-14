
from ..components.decorators import protected_page
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer

import reflex as rx

# Use @protected_page if require user login prior to viewing.
def dashboard() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),
        
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
        min_height='100vh',

    )
