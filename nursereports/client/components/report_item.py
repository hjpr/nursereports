from ...states import ReportState

import reflex as rx


def report_item_dashboard(report: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.cond(
                    report["assign_select_unit"],
                    # Report is from a unit
                    rx.cond(
                        report["assign_select_unit"] == "I don't see my unit",
                        # Report unit was entered manually.
                        rx.skeleton(
                            rx.text(
                                f"{report['assign_input_unit_name']}",
                                class_name="text-xl font-bold text-zinc-700",
                            ),
                            loading=~rx.State.is_hydrated
                        ),
                        # Report unit was selected from list.
                        rx.skeleton(
                            rx.text(
                                f"{report['assign_select_unit']}",
                                class_name="text-xl font-bold text-zinc-700",
                            ),
                            loading=~rx.State.is_hydrated
                        )
                    ),
                    # Report is from an area/role
                    rx.cond(
                        report["assign_select_area"]
                        == "I don't see my area or role",
                        # Report area/role was entered manually.
                        rx.skeleton(
                            rx.text(
                                f"{report['assign_input_area']}",
                                class_name="text-md md:text-lg font-bold text-zinc-700",
                            ),
                            loading=~rx.State.is_hydrated
                        ),
                        # Report area/role was selected from list.
                        rx.skeleton(
                            rx.text(
                                f"{report['assign_select_area']}",
                                class_name="text-md md:text-lg font-bold text-zinc-700",
                            ),
                            loading=~rx.State.is_hydrated
                        )
                    ),
                ),
                rx.skeleton(
                    rx.text(
                        f"{report.get('hosp_city')} - {report.get('hosp_state')}",
                        class_name="text-sm italic text-zinc-700"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                rx.cond(
                    report["modified_at"],
                    # Date displayed if user has made modification.
                    rx.skeleton(
                        rx.text(
                            f"Edited {report['modified_at']}",
                            class_name="text-sm italic text-zinc-700"
                        ),
                        loading=~rx.State.is_hydrated
                    ),
                    # Date displayed if user hasn't made modifications.
                    rx.skeleton(
                        rx.text(
                            f"Submitted {report['created_at']}",
                            class_name="text-sm italic text-zinc-700"
                        ),
                        loading=~rx.State.is_hydrated
                    )
                ),
                class_name="flex-col space-y-1 w-full"
            ),
            rx.spacer(),
            rx.flex(
                report_item_dashboard_remove_report(report),
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
            rx.flex(
                rx.skeleton(
                    rx.button(
                        rx.icon("trash-2", class_name="h-5 w-5"),
                        class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
                    ),
                    loading=~rx.State.is_hydrated
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
                            class_name="w-full cursor-pointer"
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


def report_item_dashboard_edit(report: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.skeleton(
            rx.button(
                rx.icon("pencil", class_name="stroke-zinc-700 h-5 w-5"),
                rx.text("Edit"),
                on_click=ReportState.event_state_edit_user_report(report["report_id"]),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer"
            ),
            loading=~rx.State.is_hydrated
        )
    )
