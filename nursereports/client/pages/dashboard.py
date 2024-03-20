
from ..components.c2a import c2a   
from ..components.custom import spacer, report_protected 
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base_state import BaseState

import reflex as rx

@rx.page(
        route='/dashboard',
        title="Nurse Reports",
        on_load=BaseState.event_state_standard_flow('report')
)
@report_protected
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
