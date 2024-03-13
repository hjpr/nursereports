
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState

import reflex as rx

@rx.page(
    route="/report/submit/[hosp_id]/complete",
    title="Nurse Reports",
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def complete_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
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
                        on_click=rx.redirect('/dashboard')
                    )
                )
            ),
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
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )