from ..components.footer import footer
from ..components.progress_bar import progress_bar
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer

import reflex as rx

def complete() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        progress_bar(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.center(
                rx.vstack(
                    rx.heading("Wow, what a healthcare hero!"),
                    rx.text(
                        """We'd throw you a pizza party, but that's a real logistical
                        nightmare, so instead check out our database of high quality
                        reports to learn about the current landscape of nursing jobs."""
                    ),
                    rx.button(
                        "Let's get started!",
                        on_click=rx.redirect('/dashboard'),
                        is_loading=~rx.State.is_hydrated
                    )
                )
            ),

            # STYLING FOR CONTENT CONTAINER
            padding_x='20px',
            width=['100%', '100%', '600px', '600px', '600px'],
            max_width='1200px',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',

        ),

        spacer(height='80px'),

        footer(),

        # STYLING FOR BODY CONTAINER
        width='100%',
        flex_direction='column',

        align_items='center',
        min_height='100vh',
    )

