
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx

@rx.page(
    route="/report/submit/[hosp_id]/compensation/summary",
    title='Nurse Reports',
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def compensation_summary_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        content(),
        spacer(height='80px'),
        footer(),
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        header(),
        spacer(height='12px'),
        compensation_summary(),
        down_arrow(),
        assignment_summary(),
        down_arrow(),
        staffing_summary(),
        spacer(height='12px'),
        buttons(),
        gap='12px',
        padding_x='20px',
        width=['100%', '500px', '500px', '500px', '500px'],
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def header() -> rx.Component:
    return rx.flex(
        rx.heading(
            "A quick primer on the sections.",
            text_align='center'
        ),
        flex_direction='column',
        width='100%',
        align_items='100%',
        justify_content='100%'
    )

def compensation_summary() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Compensation"
            ),
            rx.divider(),
            rx.text(
                """
                First, I ask you questions about pay, differentials,
                and benefits. 
                """
            )
        ),
        width='100%'
    )

def assignment_summary() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Assignment"
            ),
            rx.divider(),
            rx.text(
                """
                Next, I ask details about unit culture, the work 
                environment, and direct management.
                """
            )
        ),
        width='100%'
    )

def staffing_summary() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Staffing"
            ),
            rx.divider(),
            rx.text(
                """
                Lastly, I finish up with questions on ratios, workloads,
                and support/resources available to you.
                """
            )
        ),
        width='100%'
    )

def down_arrow() -> rx.Component:
    return rx.flex(
        rx.icon(
            'arrow-big-down',
            color='teal'
            ),
        width='100%',
        align_items='center',
        justify_content='center'
    )

def buttons() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button("Go to Compensation",
                rx.icon("arrow-big-right"),
                size='3',
                variant='ghost',
                on_click=ReportState.report_nav('compensation'),
            ),
            gap='20px',
            width='100%',
            align_items='center',
            justify_content='center'
        ),
        width='100%'
    )