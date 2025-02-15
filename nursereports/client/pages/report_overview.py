from ..components import (
    flex,
    navbar,
    login_protected,
    text,
)
from ...states import BaseState, ReportState, UserState

import reflex as rx


@rx.page(
    route="/report/[report_mode]/overview",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def overview_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        class_name="flex-col items-center dark:bg-zinc-900 min-h-screen w-full"
    )

def content() -> rx.Component:
    return rx.flex(
        hospital_info(),
        class_name="flex-col items-center space-y-12 px-4 py-4 md:py-20 w-full max-w-screen-sm",
    )

def hospital_info() -> rx.Component:
    return flex(
        # Main header
        rx.flex(
            rx.match(
                ReportState.mode,
                (
                    "edit", rx.flex(
                        text("Editing report", class_name="text-2xl font-bold"),
                        class_name="flex-row items-center space-x-2",
                    )
                ),
                (
                    "full-report", rx.flex(
                        text("Submitting Full Report", class_name="text-2xl font-bold"),
                        class_name="flex-row items-center space-x-2",
                    )
                ),
                (
                    "pay-report", rx.flex(
                        text("Submitting Pay Report", class_name="text-2xl font-bold"),
                        class_name="flex-row items-center space-x-2",
                    )
                ),
                (
                    "red-flag", rx.flex(
                        text("Red Flag Report", class_name="text-2xl font-bold"),
                        class_name="flex-row items-center space-x-2",
                    )
                )
            ),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-6 w-full"
        ),
        # Hospital header
        flex(
            flex(
                rx.skeleton(
                    text(
                        ReportState.hospital_info["hosp_name"],
                        class_name="font-bold text-center text-2xl",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                rx.skeleton(
                    text(
                        ReportState.hospital_info["hosp_addr"],
                        class_name="text-md"
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                rx.skeleton(
                    text(
                        f'{ReportState.hospital_info["hosp_city"]}, {ReportState.hospital_info["hosp_state"]} {ReportState.hospital_info["hosp_zip"]}',
                        class_name="text-md",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                class_name="flex-col items-center space-y-1 w-full",
            ),
            class_name="p-6 w-full",
        ),
        # Anonymous
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("eye", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
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
            class_name="flex-col p-6 w-full",
        ),
        # Affiliations
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("stethoscope", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
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
            class_name="flex-col p-6 w-full",
        ),
        # Time
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("clock-1", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
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
            class_name="flex-col p-6 w-full",
        ),
        # Navigation buttons
        rx.flex(
            rx.flex(
                rx.match(
                    ReportState.mode,
                    (
                        "edit", rx.flex(
                            rx.icon("arrow-left", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                            rx.text("Back", class_name="font-bold select-none"),
                            on_click=rx.redirect("/dashboard"),
                            class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                        )
                    ),
                    (
                        ("full-report" or "pay-report" or "red-flag"),
                        rx.cond(
                            UserState.user_needs_onboarding,
                            rx.flex(
                                rx.icon("arrow-left", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                                rx.text("Back", class_name="font-bold select-none"),
                                on_click=rx.redirect("/search/hospital"),
                                class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                            ),
                            rx.flex(
                                rx.icon("arrow-left", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                                rx.text("Back", class_name="font-bold select-none"),
                                on_click=rx.redirect(f"/hospital/{ReportState.hospital_id}"),
                                class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                            )
                        ),
                    )
                ),
                class_name="flex-col w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
            ),
            rx.flex(
                rx.flex(
                    rx.text("Next", class_name="font-bold select-none"),
                    rx.icon("arrow-right", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    on_click=rx.redirect(f"/report/{ReportState.mode}/compensation"),
                    class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                ),
                class_name="flex-col w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
            ),
            class_name="flex-row divide-x dark:divide-zinc-700 w-full"
        ),
        class_name="flex-col items-center border rounded shadow-lg divide-y dark:divide-zinc-700 w-full",
    )
