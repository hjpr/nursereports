
from ..state.base import State

import reflex as rx

class C2AState(State):

    # Show Call to action banner if True.
    c2a: bool = True

    # Show/close call to action.
    def toggle_c2a(self):
        self.c2a = not self.c2a

def c2a() -> rx.Component:
    """
    Conditional call to action below navbar. Shows on first visit to site
    and can be closed by user with the 'close' button.
    """
    from ..components.navbar import NavbarState
    return rx.cond(
        C2AState.c2a,
        rx.hstack(
            rx.center(
                rx.button(
                    "In Beta. Click here to submit site issue.",
                    size='sm',
                    variant='ghost',
                    color='white',
                    _hover='none',
                    on_click=NavbarState.toggle_feedback,
                ),
                width='100%',
            ),
            rx.button(
                rx.icon(
                    tag='close',
                    color='white',
                ),
                size='sm',
                variant='ghost',
                _hover='none',
                on_click=C2AState.toggle_c2a,
            ),

            # STYLING FOR C2A CONTAINER
            bg='rgba(0, 128, 128, 0.8)', # teal
            box_shadow='inset 0px 4px 5px -5px rgba(0, 0, 0, 0.5)',
            height='40px',
            padding_x='12px',
            padding_y='4px',
        ),
    )

def c2a_spacer() -> rx.Component:
    """
    Sets spacer to allow elements to move when c2a is closed.
    """
    return rx.cond(
        C2AState.c2a,
        rx.box(
            height='100px',
            width='100%',
        ),
        rx.box(
            height='60px',
            width='100%',
        ),
    )