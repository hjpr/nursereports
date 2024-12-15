from .tailwind import (
    flex,
    outline_button,
    text
)

from ...states import ReportState

import reflex as rx


def report_item_dashboard(report: dict[str, str]) -> rx.Component:
    return flex(
        flex(
            flex(
                rx.cond(
                    report["assign_select_specific_unit"] == "Yes",

                    # Report is from a unit
                    rx.cond(
                        report["assign_select_unit"],

                        # Report unit was selected from list.
                        rx.skeleton(
                            text(
                                f"{report['assign_select_unit']}",
                                class_name="text-xl font-bold",
                            ),
                            loading=~rx.State.is_hydrated
                        ),

                        # Report unit was entered manually.
                        rx.skeleton(
                            text(
                                f"{report['assign_input_unit_name']}",
                                class_name="text-xl font-bold",
                            ),
                            loading=~rx.State.is_hydrated
                        )
                    ),

                    # Report is from an area/role
                    rx.cond(
                        report["assign_select_area"],

                        # Report area/role was selected from list.
                        rx.skeleton(
                            rx.text(
                                f"{report['assign_select_area']}",
                                class_name="text-md md:text-lg font-bold text-zinc-700",
                            ),
                            loading=~rx.State.is_hydrated
                        ),

                        # Report area/role was entered manually.
                        rx.skeleton(
                            text(
                                f"{report['assign_input_area']}",
                                class_name="text-md md:text-lg font-bold",
                            ),
                            loading=~rx.State.is_hydrated
                        )
                    )
                ),
                rx.skeleton(
                    text(
                        f"{report['hosp_city']} - {report['hosp_state']}",
                        class_name="text-sm italic"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                rx.cond(
                    report["modified_at"],
                    # Date displayed if user has made modification.
                    rx.skeleton(
                        text(
                            f"Edited {report['modified_at']}",
                            class_name="text-sm italic"
                        ),
                        loading=~rx.State.is_hydrated
                    ),
                    # Date displayed if user hasn't made modifications.
                    rx.skeleton(
                        text(
                            f"Submitted {report['created_at']}",
                            class_name="text-sm italic"
                        ),
                        loading=~rx.State.is_hydrated
                    )
                ),
                class_name="flex-col space-y-1 w-full"
            ),
            rx.spacer(),
            flex(
                report_item_dashboard_edit(report),
                class_name="space-x-2"
            ),
            class_name="flex-row items-center space-x-4 w-full"
        ),
        class_name="p-4 w-full"
    )


def report_item_dashboard_remove_report(report: dict[str, str]) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            flex(
                rx.skeleton(
                    outline_button(
                        rx.icon("trash-2", class_name="h-5 w-5"),
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
                            class_name="w-full cursor-pointer"
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


def report_item_dashboard_edit(report: dict[str, str]) -> rx.Component:
    return flex(
        rx.skeleton(
            outline_button(
                rx.icon("pencil", class_name="h-5 w-5"),
                rx.text("Edit"),
                on_click=ReportState.event_state_edit_user_report(report["report_id"]),
            ),
            loading=~rx.State.is_hydrated
        )
    )
