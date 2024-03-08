
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx

@rx.page(
    route="/report/submit/[report_id]/staffing/summary",
    title='Nurse Reports',
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def staffing_summary_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        rx.flex(
            rx.vstack(
                staffing_summary(),
                spacer(height='40px'),
                buttons(),
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

def staffing_summary() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Staffing"
            ),
            rx.divider(),
            rx.text(
                """Lastly, we'll ask questions in a category called staffing.
                This covers issues like staffing ratios (if applicable),
                workloads, and availability of support staff.
                """,
                text_align='center'
            )
        )
    )

def buttons() -> rx.Component:
    return rx.center(
        rx.button("Back",
            width='100%',
            on_click=ReportState.report_nav('assignment'),
        ),
        rx.button("Next",
            width='100%',
            on_click=ReportState.report_nav('staffing'),
        ),
        width='50%',
    )