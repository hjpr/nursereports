
from ..components import (
    c2a,
    footer,
    login_protected,
    navbar,
)
from ...states import BaseState, ReportState

import reflex as rx

@rx.page(
    route="/report/edit/staffing/",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_standard_flow("login"),
        ReportState.event_state_report_flow
        ],
)
@login_protected
def edit_staffing_page() -> rx.Component:
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
        
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )