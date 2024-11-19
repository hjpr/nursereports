from ..components import (
    c2a,
    footer,
    hospital_item_dashboard,
    navbar,
    report_item_dashboard,
    report_protected,
)
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/dashboard",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("report"),
    ],
)
@report_protected
def dashboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-teal-50 w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        heading(),
        saved_hospitals(),
        my_pay(),
        my_reports(),
        class_name="flex-col items-center p-4 pt-8 pb-8 space-y-8 w-full max-w-screen-md",
    )


def heading() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("layout-dashboard", class_name="h-6 w-6 stroke-teal-800"),
            rx.text("Dashboard", class_name="text-2xl font-bold text-zinc-800"),
            class_name="flex-row items-center space-x-2",
        ),
        class_name="flex-col items-center border rounded bg-zinc-100 p-4 w-full",
    )


def saved_hospitals() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("hospital", class_name="h-5 w-5"),
                    rx.text("Saved Hospitals", class_name="text-xl font-bold"),
                    class_name="flex-row items-center text-zinc-700 space-x-2",
                ),
                class_name="flex-row items-center bg-zinc-100 p-2 w-full",
            ),
            rx.cond(
                BaseState.saved_hospitals,
                # User has saved hospitals.
                rx.flex(
                    rx.foreach(BaseState.saved_hospitals, hospital_item_dashboard),
                    class_name="flex-col divide-y w-full",
                ),
                # User doesn't have saved hospitals.
                rx.flex(
                    rx.button(
                        rx.icon("search", class_name="h-5 w-5"),
                        "Find hospitals to add...",
                        on_click=rx.redirect("/search/hospital"),
                        class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                    ),
                    class_name="flex-col items-center justify-center w-full min-h-[92px]",
                ),
            ),
            class_name="flex-col divide-y w-full",
        ),
        class_name="border rounded bg-white w-full",
    )


def skeleton_hospitals(hospital: dict) -> rx.Component:
    return rx.flex(rx.skeleton(), class_name="w-full h-[96px]")


def my_pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.icon("piggy-bank", class_name="h-5 w-5 stroke-zinc-700"),
                rx.text("My Pay", class_name="text-xl font-bold text-zinc-700"),
                class_name="flex-row items-center bg-zinc-100 space-x-2 p-2 w-full",
            ),
            rx.flex(
                rx.text("PLACEHOLDER", class_name="text-sm"),
                class_name="flex-col items-center justify-center w-full min-h-[300px]",
            ),
            class_name="flex-col divide-y w-full",
        ),
        class_name="border rounded bg-white w-full",
    )


def my_reports() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.icon("file-text", class_name="h-5 w-5 stroke-zinc-700"),
                rx.text("My Reports", class_name="text-xl font-bold text-zinc-700"),
                class_name="flex-row items-center bg-zinc-100 space-x-2 p-2 w-full",
            ),
            rx.cond(
                BaseState.user_reports,
                # User has prior reports.
                rx.flex(
                    rx.foreach(BaseState.user_reports, report_item_dashboard),
                    class_name="flex-col divide-y w-full",
                ),
                # User doesn't have prior reports.
                rx.flex(
                    rx.button(
                        rx.icon("search", class_name="h-5 w-5"),
                        "Make a report...",
                        on_click=rx.redirect("/search/hospital"),
                        class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                    ),
                    class_name="flex-col items-center justify-center w-full min-h-[92px]",
                ),
            ),
            class_name="flex-col divide-y w-full",
        ),
        class_name="border rounded bg-white w-full",
    )
