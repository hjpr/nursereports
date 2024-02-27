
from ...states import *

import reflex as rx

def c2a() -> rx.Component:
    return rx.cond(
        BaseState.user_is_authenticated,
        rx.box(
            rx.hstack(
                rx.center(
                    rx.button(
                        "In Beta. Click here to submit issue or feedback.",
                        cursor='pointer',
                        color='white',
                        color_scheme='crimson',
                        on_click=NavbarState.set_show_feedback(True)
                    ),
                    width='100%'
                ),
                bg='#E93D82',
                height='40px',
                padding_x='12px',
                padding_y='4px'
            ),
            width='100%'
        )
    )