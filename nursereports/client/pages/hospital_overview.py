
from ..components import (
    c2a,
    footer,
    login_protected,
    navbar,
)
from ...states import BaseState

import reflex as rx

@rx.page(
    route="/hospital/[hosp_id]",
    title="Nurse Reports",
    on_load=BaseState.event_state_standard_flow("login"),
)
@login_protected
def hospital_overview() -> rx.Component:
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
        rx.text("Hospital Overview Placeholder Page"),
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )