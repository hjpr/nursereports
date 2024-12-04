from .tailwind import (
    flex,
    outline_button,
    text
)

from ...states import HospitalState, ReportState, UserState

import reflex as rx


def hospital_item_search(hospital: dict[str, str]) -> rx.Component:
    return flex(
        flex(
            flex(
                rx.skeleton(
                    text(
                        f"{hospital['hosp_name']}",
                        class_name="text-md md:text-lg font-bold text-zinc-700"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                rx.skeleton(
                    text(
                        f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                        class_name="text-sm italic text-zinc-600"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                class_name="flex-col space-y-1"
            ),
            rx.spacer(),
            flex(
                save_hospital(hospital),
                go_to_report(hospital),
                class_name="space-x-2"
            ),
            class_name="flex-row items-center w-full"
        ),
        class_name="p-4 w-full"
    )


def save_hospital(hospital: dict[str, str]) -> rx.Component:
    return flex(
        rx.tooltip(
            rx.skeleton(
                outline_button(
                    rx.icon("list-plus"),
                    on_click=UserState.event_state_add_hospital(hospital['hosp_id']),
                ),
                loading=~rx.State.is_hydrated
            ),
            content="Add to Saved Hospitals"
        )
    )


def go_to_report(hospital: dict[str, str]) -> rx.Component:
    return rx.cond(
        UserState.user_has_reported,
        rx.box(
            rx.skeleton(
                outline_button(
                    rx.text("Go"),
                    rx.icon("arrow-right", class_name="h-4 w-4"),
                    disabled=~rx.State.is_hydrated,
                    on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id']),
                ),
                loading=~rx.State.is_hydrated
            )
        ),
        rx.box(
            rx.skeleton(
                outline_button(
                    rx.text("Go"),
                    rx.icon("arrow-right", class_name="h-4 w-4"),
                    disabled=~rx.State.is_hydrated,
                    on_click=ReportState.event_state_create_full_report(hospital['hosp_id']),
                ),
                loading=~rx.State.is_hydrated
            )
        )
    )


def hospital_item_dashboard(hospital: dict[str, str]) -> rx.Component:
    return flex(
        flex(
            flex(
                rx.skeleton(
                    text(
                        f"{hospital['hosp_name']}",
                        class_name="text-md md:text-lg font-bold"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                rx.skeleton(
                    text(
                        f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                        class_name="text-sm italic"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                class_name="flex-col space-y-1"
            ),
            rx.spacer(),
            flex(
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
            flex(
                rx.skeleton(
                    outline_button(
                        rx.icon("trash-2", class_name="h-5 w-5"),
                        disabled=~rx.State.is_hydrated,
                        class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                    ),
                    loading=~rx.State.is_hydrated
                )
            )
        ),
        rx.popover.content(
            flex(
                rx.text("Are you sure?"),
                rx.popover.close(
                    flex(
                        rx.button(
                            "Delete",
                            color_scheme="ruby",
                            class_name="w-full cursor-pointer",
                            on_click=UserState.event_state_remove_hospital(hospital['hosp_id'])
                        ),
                        outline_button(
                            "Cancel",
                        ),
                        class_name="flex-col space-y-4 w-full"
                    )
                ),
                class_name="flex-col items-center space-y-4"
            )
        )
    )


def dashboard_arrow(hospital: dict[str, str]) -> rx.Component:
    return flex(
        rx.skeleton(
            outline_button(
                rx.text("Go"),
                rx.icon("arrow-right", class_name="h-5 w-5"),
                disabled=~rx.State.is_hydrated,
                on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id']),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer"
            ),
            loading=~rx.State.is_hydrated
        )
    )