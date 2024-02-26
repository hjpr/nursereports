
from ..states.base import BaseState
from ..states.navbar import NavbarState

import reflex as rx

def c2a() -> rx.Component:
    """
    Renders call to action bar if NavbarState.show_c2a is True and
    the user is logged in.
    """
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