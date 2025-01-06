from ..components import (
    flex,
    footer,
    navbar,
    login_protected,
    outline_button,
    solid_button,
    text,
)
from ...states import BaseState, ReportState

import reflex as rx


@rx.page(
    route="/report/full-report/overview",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def overview_page() -> rx.Component:
    return flex(navbar(), content(), footer(), class_name="flex-col items-center")


def content() -> rx.Component:
    return flex(
        header(),
        hospital_info(),
        buttons(),
        class_name="flex-col items-center space-y-12 px-4 py-12 w-full max-w-screen-md",
    )


def header() -> rx.Component:
    return rx.flex(
        rx.flex(
            text("Submit Full Report", class_name="text-2xl font-bold"),
            class_name="flex-row items-center space-x-2",
        ),
        class_name="flex-col items-center border rounded bg-zinc-100 dark:bg-zinc-800 p-4 w-full",
    )


def hospital_info() -> rx.Component:
    return rx.flex(
        # Hospital header
        rx.flex(
            flex(
                rx.skeleton(
                    text(
                        ReportState.hospital_info["hosp_name"],
                        class_name="font-bold text-center text-2xl",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                rx.skeleton(
                    text(ReportState.hospital_info["hosp_addr"], class_name="text-sm"),
                    loading=~rx.State.is_hydrated,
                ),
                rx.skeleton(
                    text(
                        f'{ReportState.hospital_info["hosp_city"]}, {ReportState.hospital_info["hosp_state"]} {ReportState.hospital_info["hosp_zip"]}',
                        class_name="text-sm",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                class_name="flex-col items-center space-y-1 w-full",
            ),
            class_name="p-4 w-full",
        ),
        # Anonymous
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("eye"),
                    class_name="flex-col justify-center items-center h-8 w-8",
                ),
                text(
                    """
                    All reporting is anonymous. No personal details
                    are attached to your report.
                    """,
                ),
                class_name="flex-row justify-start items-center space-x-4 w-full",
            ),
            class_name="flex-col p-4 w-full",
        ),
        # Affiliations
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("stethoscope"),
                    class_name="flex-col justify-center items-center h-8 w-8",
                ),
                text(
                    """
                    I am not affiliated with hospital interests. These reports are gathered
                    for the benefit of the nursing community across the US.
                    """,
                ),
                class_name="flex-row justify-start items-center space-x-4 w-full",
            ),
            class_name="flex-col p-4 w-full",
        ),
        # Time
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("clock-1"),
                    class_name="flex-col justify-center items-center h-8 w-8",
                ),
                text(
                    """
                    Your time is valuable. This should only take
                    about 5 minutes. 
                    """,
                ),
                class_name="flex-row justify-start items-center space-x-4 w-full",
            ),
            class_name="flex-col p-4 w-full",
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full",
    )


def buttons() -> rx.Component:
    return rx.flex(
        outline_button(
            rx.icon("arrow-big-left"),
            "Go back",
            on_click=rx.call_script("window.history.back()"),
        ),
        solid_button(
            "Let's go!",
            rx.icon("arrow-big-right"),
            on_click=rx.redirect("/report/full-report/compensation"),
        ),
        class_name="flex-row justify-center items-center border rounded space-x-4 p-4 w-full",
    )
