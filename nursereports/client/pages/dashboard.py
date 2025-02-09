from ..components import (
    flex,
    footer,
    hospital_item_dashboard,
    navbar,
    report_item_dashboard,
    report_protected,
    text,
)
from ...states import BaseState, UserState

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
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        heading(),
        saved_hospitals(),
        my_pay(),
        my_reports(),
        class_name="flex-col items-center space-y-4 md:space-y-12 px-4 py-4 md:py-12 w-full md:max-w-screen-md",
    )


def heading() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("layout-dashboard", class_name="h-6 w-6 stroke-teal-800"),
            text("Dashboard", class_name="text-2xl font-bold"),
            class_name="bg-transparent flex-row items-center space-x-2",
        ),
        class_name="flex-col items-center border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 p-4 w-full",
    )


def saved_hospitals() -> rx.Component:
    return rx.flex(
        flex(
            rx.flex(
                rx.flex(
                    rx.icon("hospital", class_name="h-5 w-5 stroke-zinc-700 dark:stroke-teal-800"),
                    text("Saved Hospitals", class_name="text-xl font-bold"),
                    class_name="flex-row items-center space-x-2",
                ),
                class_name="flex-row items-center bg-zinc-100 dark:bg-zinc-800 p-2 w-full",
            ),
            rx.cond(
                UserState.user_saved_hospitals,
                # User has saved hospitals.
                flex(
                    rx.foreach(BaseState.user_saved_hospitals, hospital_item_dashboard),
                    class_name="flex-col divide-y dark:divide-zinc-500 w-full",
                ),
                # User doesn't have saved hospitals.
                flex(
                    rx.icon("ellipsis", class_name="stroke-zinc-700"),
                    class_name="flex-col items-center justify-center w-full min-h-[92px]",
                ),
            ),
            class_name="flex-col divide-y dark:divide-zinc-500 w-full",
        ),
        class_name="border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 w-full",
    )


def skeleton_hospitals(hospital: dict) -> rx.Component:
    return flex(rx.skeleton(), class_name="w-full h-[96px]")


def my_pay() -> rx.Component:
    return rx.flex(
        flex(
            rx.flex(
                rx.icon("piggy-bank", class_name="h-5 w-5 stroke-zinc-700 dark:stroke-teal-800"),
                text("My Pay", class_name="text-xl font-bold text-zinc-700"),
                class_name="flex-row items-center bg-zinc-100 dark:bg-zinc-800 space-x-2 p-2 w-full",
            ),
            flex(
                rx.icon("ellipsis", class_name="stroke-zinc-700"),
                class_name="flex-col items-center justify-center w-full min-h-[300px]",
            ),
            class_name="flex-col divide-y dark:divide-zinc-500 w-full",
        ),
        class_name="border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 w-full",
    )


def my_reports() -> rx.Component:
    return rx.flex(
        flex(
            rx.flex(
                rx.icon("file-text", class_name="h-5 w-5 stroke-zinc-700 dark:stroke-teal-800"),
                text("My Reports", class_name="text-xl font-bold"),
                class_name="flex-row items-center bg-zinc-100 dark:bg-zinc-800 space-x-2 p-2 w-full",
            ),
            rx.cond(
                UserState.user_reports,
                flex(
                    rx.foreach(BaseState.user_reports, report_item_dashboard),
                    class_name="flex-col divide-y w-full",
                ),
                flex(
                    rx.icon("ellipsis", class_name="stroke-zinc-700"),
                    class_name="flex-col items-center justify-center w-full min-h-[92px]",
                ),
            ),
            class_name="flex-col divide-y dark:divide-zinc-500 w-full",
        ),
        class_name="border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 w-full",
    )
