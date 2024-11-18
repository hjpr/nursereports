
from ...states import BaseState, HospitalState, ReportState

import reflex as rx


def hospital_item_search(hospital: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text(
                    f"{hospital['hosp_name']}",
                    class_name="text-md md:text-lg font-bold text-zinc-700"
                ),
                rx.text(
                    f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                    class_name="text-sm md:text-md italic text-zinc-600"
                ),
                class_name="flex-col space-y-2 w-full"
            ),
            rx.spacer(),
            rx.flex(
                save_hospital(hospital),
                go_to_report(hospital),
                class_name="space-x-2"
            ),
            class_name="flex-row items-center w-full"
        ),
        class_name="p-4 w-full"
    )


def save_hospital(hospital: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.tooltip(
            rx.button(
                rx.icon("list-plus"),
                on_click=BaseState.event_state_add_hospital(hospital['hosp_id']),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
            ),
            content="Add to Saved Hospitals"
        )
    )


def go_to_report(hospital: dict[str, str]) -> rx.Component:
    return rx.cond(
        BaseState.user_has_reported,
        rx.box(
            rx.button(
                rx.text("Go"),
                rx.icon("arrow-right", class_name="h-4 w-4"),
                on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id']),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
            )
        ),
        rx.box(
            rx.button(
                rx.text("Go"),
                rx.icon("arrow-right", class_name="h-4 w-4"),
                on_click=ReportState.event_state_create_full_report(hospital['hosp_id']),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
            )
        )
    )


def hospital_item_dashboard(hospital: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text(
                    f"{hospital['hosp_name']}",
                    class_name="text-lg font-bold text-zinc-700"
                ),
                rx.text(
                    f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                    class_name="text-md italic"
                ),
                class_name="flex-col"
            ),
            rx.spacer(),
            rx.flex(
                dashboard_trash(hospital),
                dashboard_arrow(hospital),
                class_name="space-x-2"
            ),
            class_name="flex-row items-center space-x-4 w-full"
        ),
        class_name="p-4 w-full"
    )


def dashboard_trash(hospital: dict[str, str]) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                rx.button(
                    rx.icon("trash-2", class_name="h-5 w-5"),
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                )
            )
        ),
        rx.popover.content(
            rx.flex(
                rx.text("Are you sure?"),
                rx.popover.close(
                    rx.flex(
                        rx.button(
                            "Delete",
                            color_scheme="ruby",
                            class_name="w-full cursor-pointer",
                            on_click=BaseState.event_state_remove_hospital(hospital['hosp_id'])
                        ),
                        rx.button(
                            "Cancel",
                            class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                        ),
                        class_name="flex-col space-y-4 w-full"
                    )
                ),
                class_name="flex-col items-center space-y-4"
            )
        )
    )


def dashboard_arrow(hospital: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.button(
            rx.text("Go"),
            rx.icon("arrow-right", class_name="h-5 w-5"),
            on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id']),
            class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer"
        )
    )