from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base_state import BaseState
from ...states.report_state import ReportState

import reflex as rx


@rx.page(
    route="/report/full-report/outline",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
        ReportState.event_state_report_flow
    ]
)
@login_protected
def outline_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height="40px"),
        content(),
        spacer(height="80px"),
        footer(),
        width="100%",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        spacer(height="12px"),
        compensation_summary(),
        down_arrow(),
        assignment_summary(),
        down_arrow(),
        staffing_summary(),
        spacer(height="36px"),
        buttons(),
        gap="12px",
        padding_x="20px",
        width=["100%", "500px", "500px", "500px", "500px"],
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def header() -> rx.Component:
    return rx.flex(
        rx.heading("A quick primer on the 3 sections.", text_align="center"),
        flex_direction="column",
        width="100%",
        align_items="100%",
        justify_content="100%",
    )


def compensation_summary() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("1. Compensation"),
            rx.divider(),
            rx.text(
                """
                First, I ask you questions about pay, differentials,
                and benefits offered. 
                """
            ),
        ),
        width="100%",
    )


def assignment_summary() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("2. Assignment"),
            rx.divider(),
            rx.text(
                """
                Next, I ask details about unit culture, the work 
                environment, and nursing leadership.
                """
            ),
        ),
        width="100%",
    )


def staffing_summary() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("3. Staffing"),
            rx.divider(),
            rx.text(
                """
                Lastly, I finish up with questions on patient ratios,
                workloads, and resources available to you.
                """
            ),
        ),
        width="100%",
    )


def down_arrow() -> rx.Component:
    return rx.flex(
        rx.icon("arrow-big-down", color="teal"),
        width="100%",
        align_items="center",
        justify_content="center",
    )


def buttons() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Go to Compensation",
                rx.icon("arrow-big-right"),
                size="3",
                variant="ghost",
                on_click=rx.redirect("/report/full-report/compensation"),
            ),
            gap="20px",
            width="100%",
            align_items="center",
            justify_content="center",
        ),
        width="100%",
    )
