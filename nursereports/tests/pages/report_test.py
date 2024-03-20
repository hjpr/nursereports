
from ...client.components import c2a
from ...client.components.custom import spacer, login_protected
from ...client.components.footer import footer
from ...client.components.navbar import navbar
from ...states.base_state import BaseState
from ...states.report_state import ReportState
from ..states.test_state import ReportTestState

import reflex as rx

@rx.page(
    route="/report/submit/[hosp_id]/test",
    title='Nurse Reports',
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def test_page() -> rx.Component:
    return rx.flex(
    c2a(),
    navbar(),
    spacer(height='1em'),
    content(),
    spacer(height='1em'),
    footer(),
    width='100%',
    flex_direction='column',
    align_items='center',
    min_height='100vh',
)

def content() -> rx.Component:
    return rx.flex(
        information(),
        user_inputs(),
        regenerate(),
        button(),
        callouts(),
        gap='24px',
        padding_x='24px',
        width=['100%', '480px', '480px', '480px', '480px'],
        max_width='1200px',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def information() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading(
                "Report Test"
            ),
            spacer(height='8px'),
            rx.divider(),
            spacer(height='24px'),
            rx.text(
                """Test out user inputs quickly. Enter user inputs below
                to recieve error messages regarding specifically those
                user inputs.
                """
            ),
            flex_direction='column',
            width='100%'
        )
    )

def user_inputs() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.flex(
                rx.text(
                    "Compensation user comments."
                ),
                rx.debounce_input(
                    rx.text_area(
                        value=ReportTestState.comp_input_comments,
                        on_change=ReportTestState.set_comp_input_comments,
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%',
                    debounce_timeout=1000
                ),
                flex_direction='column',
                gap='8px',
                width='100%'
            ),
            rx.flex(
                rx.text(
                    "Unit name."
                ),
                rx.debounce_input(
                    rx.input(
                        value=ReportTestState.assign_input_unit_name,
                        on_change=ReportTestState.set_assign_input_unit_name,
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%',
                    debounce_timeout=1000
                ),
                flex_direction='column',
                gap='8px',
                width='100%'
            ),
            rx.flex(
                rx.text(
                    "Area/role name."
                ),
                rx.debounce_input(
                    rx.input(
                        value=ReportTestState.assign_input_area,
                        on_change=ReportTestState.set_assign_input_area,
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%',
                    debounce_timeout=1000
                ),
                flex_direction='column',
                gap='8px',
                width='100%'
            ),
            rx.flex(
                rx.text(
                    "Assignment user comments."
                ),
                rx.debounce_input(
                    rx.text_area(
                        value=ReportTestState.assign_input_comments,
                        on_change=ReportTestState.set_assign_input_comments,
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%',
                    debounce_timeout=1000
                ),
                flex_direction='column',
                gap='8px',
                width='100%'
            ),
            rx.flex(
                rx.text(
                    "Staffing user comments."
                ),
                rx.debounce_input(
                    rx.text_area(
                        value=ReportTestState.staffing_input_comments,
                        on_change=ReportTestState.set_staffing_input_comments,
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%',
                    debounce_timeout=1000
                ),
                flex_direction='column',
                gap='8px',
                width='100%'
            ),
            width='100%',
            flex_direction='column',
            gap='24px'
        ),
        width='100%'
    )

def regenerate() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Regenerate Report ID",
                rx.icon("arrow-big-right"),
                on_click=ReportState.generate_report_id,
                variant='ghost',
                size='3'
            ),
            align_items='center',
            justify_content='center',
            width='100%',
        ),
        width='100%'
    )

def button() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                rx.cond(
                    ReportTestState.is_running,
                    rx.chakra.spinner(),
                    rx.text("Submit Report for Test")
                ),
                rx.icon("arrow-big-right"),
                on_click=ReportTestState.event_test_report,
                variant='ghost',
                size='3'
            ),
            align_items='center',
            justify_content='center',
            width='100%',
        ),
        width='100%'
    )

def callouts() -> rx.Component:
    return rx.flex(
        rx.cond(
            ReportState.staffing_has_error,
            rx.callout(
                ReportState.staffing_error_message,
                width='100%',
                icon='alert_triangle',
                color_scheme='red',
                role='alert'
            )
        ),
        width='100%',
        flex_direction='column',
        gap='24px'
    )