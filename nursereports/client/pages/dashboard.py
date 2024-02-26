
from ..components.c2a import c2a    
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.custom import spacer
from ...states.base import BaseState

import reflex as rx

@rx.page(
        route='/dashboard',
        title="Nurse Reports",
        on_load=BaseState.standard_flow('req_report')
)
def dashboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        rx.flex(
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
        ),
        footer(),
        flex_direction='column',
        min_height='100vh',
    )
