
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx

@rx.page(
    route="/report/submit/[report_id]/assignment/summary",
    title='Nurse Reports',
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def assign_summary_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        rx.flex(
            rx.vstack(
                assignment_summary(),
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

def assignment_summary() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Assignment"
            ),
            rx.divider(),
            rx.text(
                """Next, we'll ask questions in a category called assignment.
                This covers details about the area or unit you are assigned
                to like culture, environment, and management.

                We'll ask about ratios and workload in the section after 
                this one.
                """,
                text_align='center'
            )
        )
    )

def buttons() -> rx.Component:
    return rx.center(
        rx.button("Back",
                width='100%',
                on_click=ReportState.report_nav('compensation'),
        ),
        rx.button("Next",
                width='100%',
                on_click=ReportState.report_nav('assignment'),
        ),
        width='50%',
    )
