
from ...states import BaseState, HospitalState, ReportState

import reflex as rx


def hospital_item_search(hospital: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text(
                    f"{hospital['hosp_name']}",
                    class_name="text-md md:text-xl font-bold text-zinc-700"
                ),
                rx.text(
                    f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                    class_name="text-md md:text-lg italic text-zinc-600"
                ),
                class_name="flex-col space-y-2 p-4 w-full"
            ),
            rx.spacer(),
            rx.flex(
                rx.flex(
                    hospital_item_search_arrow(hospital),
                    class_name="flex-col items-center justify-center p-4"
                ),
            ),
            class_name="flex-row w-full"
        ),
        class_name="w-full min-w-36"
    )


def hospital_item_dashboard(hospital: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text(
                    f"{hospital['hosp_name']}",
                    font_weight="bold",
                    font_size=["16px", "16px", "18px", "18px", "18px"],
                    line_height="1em"
                ),
                rx.text(
                    f"{hospital['hosp_city']}, {hospital['hosp_state']}",
                    font_size="14px",
                    font_style="italic",
                ),
                height="100%",
                width="100%",
                flex_direction="column",
                justify="center",
                gap=["4px", "4px", "12px", "12px", "12px"],
                padding="12px"
            ),
            rx.spacer(),
            rx.flex(
                hospital_item_dashboard_trash(hospital),
                align="center",
                justify="center",
                height="100%",
                min_height="100px",
                min_width=["50px", "50px", "100px", "100px", "100px"],
            ),
            rx.flex(
                hospital_item_dashboard_arrow(hospital),
                align="center",
                justify="center",
                height="100%",
                min_height="100px",
                min_width=["50px", "50px", "100px", "100px", "100px"],
                border_left="1px solid var(--chakra-colors-chakra-border-color)"
            ),
            flex_direction="row",
            width="100%",
        ),
        min_height="100px",
        width="100%",
    )


def hospital_item_search_arrow(hospital: dict[str, str]) -> rx.Component:
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
                rx.icon("arrow-right"),
                on_click=ReportState.event_state_create_full_report(hospital['hosp_id']),
            )
        )
    )


def hospital_item_search_dropdown(hospital: dict[str, str]) -> rx.Component:
    return rx.cond(
        BaseState.user_has_reported,
        rx.box(
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.icon("ellipsis-vertical"),
                        variant="ghost",
                        cursor="pointer"
                    )
                ),
                rx.menu.content(
                    rx.menu.item(
                        "Save to My Hospitals",
                        on_click=BaseState.event_state_add_hospital(hospital['hosp_id'])
                        ),
                    rx.menu.separator(),
                    rx.menu.item(
                        "Submit Full Report",
                        on_click=ReportState.event_state_create_full_report(hospital['hosp_id'])
                    ),
                    rx.menu.item(
                        "Submit Red Flag Report",
                        on_click=ReportState.redirect_to_red_flag_report(hospital['hosp_id'])
                    )
                )
            )
        )
    )


def hospital_item_dashboard_arrow(hospital: dict[str, str]) -> rx.Component:
    return rx.button(
        rx.icon("arrow-right"),
        variant="ghost",
        cursor="pointer",
        on_click=HospitalState.redirect_to_hospital_overview(hospital['hosp_id'])
    )


def hospital_item_dashboard_trash(hospital: dict[str, str]) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.icon("trash-2"),
                variant="ghost",
                cursor="pointer"
            )
        ),
        rx.popover.content(
            rx.flex(
                rx.text("Are you sure?"),
                rx.popover.close(
                    rx.vstack(
                        rx.button(
                            "Delete",
                            width="100%",
                            size="3",
                            color_scheme="ruby",
                            on_click=BaseState.event_state_remove_hospital(hospital['hosp_id'])
                        ),
                        rx.button(
                            "Cancel",
                            width="100%",
                            size="3",
                            variant="ghost"
                        )
                    )
                ),
                flex_direction="column",
                align="center",
                justify="center",
                spacing="3"
            )
        )
    )