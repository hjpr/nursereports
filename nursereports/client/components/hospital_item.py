from .tailwind import (
    flex,
    outline_button,
    text
)

from ...states import HospitalState, ReportState, UserState

import reflex as rx


def hospital_item_search(hospital: dict[str, str]) -> rx.Component:
    return flex(
        rx.flex(
            # Contains hospital info
            rx.skeleton(
                text(
                    f"{hospital['hosp_name']}",
                    class_name="text-md md:text-lg font-bold text-zinc-700 truncate"
                ),
                loading=~rx.State.is_hydrated
            ),
            rx.skeleton(
                text(
                    f"{hospital['hosp_addr']}",
                    class_name="text-sm italic text-zinc-600 truncate"
                ),
                loading=~rx.State.is_hydrated
            ),
            rx.skeleton(
                text(
                    f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                    class_name="text-sm italic text-zinc-600 truncate"
                ),
                loading=~rx.State.is_hydrated
            ),
            class_name="flex-col flex-1 min-w-0 justify-center p-4"
        ),
        rx.flex(
            # Save hospitals button if user doesn't need onboarding.
            rx.cond(
                ~UserState.user_needs_onboarding,
                rx.flex(
                    rx.tooltip(
                        rx.skeleton(
                            rx.button(
                                rx.icon("list-plus", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                                class_name="w-full h-full p-0 bg-zinc-50 active:bg-zinc-100 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                                loading=UserState.user_is_loading,
                                on_click=UserState.add_hospital_to_user_list(hospital['hosp_id']),
                            ),
                            loading=~rx.State.is_hydrated
                        ),
                        content="Add to Saved Hospitals"
                    ),
                    class_name="flex-col items-center justify-center w-16 md:w-24"
                ),
            ),
            # Go to report button
            rx.cond(
                UserState.user_needs_onboarding,
                rx.flex(
                    rx.skeleton(
                        rx.flex(
                            rx.icon("arrow-right", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                        ),
                        loading=~rx.State.is_hydrated
                    ),
                    on_click=ReportState.event_state_create_full_report(hospital['hosp_id']),
                    class_name="flex-col items-center justify-center w-16 md:w-24 active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
                ),
                rx.flex(
                    rx.skeleton(
                        rx.flex(
                            rx.icon("arrow-right", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                        ),
                        loading=~rx.State.is_hydrated
                    ),
                    on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id']),
                    class_name="flex-col items-center justify-center w-16 md:w-24 active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
                )
            ),
        ),
        class_name="flex-row justify-between w-full"
    )


def hospital_item_dashboard(hospital: dict[str, str]) -> rx.Component:
    return flex(
        rx.flex(
            # Contains hospital info
            rx.skeleton(
                text(
                    f"{hospital['hosp_name']}",
                    class_name="text-md font-bold text-zinc-700 truncate"
                ),
                loading=~rx.State.is_hydrated
            ),
            rx.skeleton(
                text(
                    f"{hospital['hosp_addr']}",
                    class_name="text-sm italic text-zinc-600 truncate"
                ),
                loading=~rx.State.is_hydrated
            ),
            rx.skeleton(
                text(
                    f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                    class_name="text-sm italic text-zinc-600 truncate"
                ),
                loading=~rx.State.is_hydrated
            ),
            class_name="flex-col flex-1 min-w-0 justify-center p-4"
        ),
        rx.flex(
            dashboard_trash(hospital),
            dashboard_arrow(hospital),
        ),
        class_name="flex-row justify-between w-full"
    )


def dashboard_trash(hospital: dict[str, str]) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            flex(
                rx.skeleton(
                    rx.icon("trash-2", class_name="h-5 w-5 stroke-zinc-700 dark:stroke-zinc-500"),
                    loading=~rx.State.is_hydrated,
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                ), 
                class_name="flex-col items-center justify-center w-16 md:w-24 active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
            ),
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
                            loading=UserState.user_is_loading,
                            on_click=UserState.remove_hospital_from_saved(hospital['hosp_id']),
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
    return rx.flex(
        rx.skeleton(
            rx.icon("arrow-right", class_name=" h-5 w-5 stroke-zinc-700 dark:stroke-zinc-500"),
            loading=~rx.State.is_hydrated,
            class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer"
        ),
        on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id']),
        class_name="flex-col items-center justify-center w-16 md:w-24 active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
    )