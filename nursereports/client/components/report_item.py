from .tailwind import flex, outline_button, text

from ...states import ReportState

import reflex as rx


def report_item_dashboard(report: dict) -> rx.Component:
    return flex(
        rx.flex(
            # Unit/area/role
            rx.skeleton(
                text(
                    f"{report['unit']}{report['area']}{report['role']}",
                    class_name="text-md font-bold",
                ),
                loading=~rx.State.is_hydrated,
            ),
            # City/state
            rx.skeleton(
                text(
                    f"{report['hospital_city']}, {report['hospital_state']}",
                    class_name="text-sm italic",
                ),
                loading=~rx.State.is_hydrated,
            ),
            # Modified at
            rx.cond(
                report["modified_at"],
                # Date displayed if user has made modification.
                rx.skeleton(
                    text(
                        f"Edited {report['time_ago']}",
                        class_name="text-sm italic",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                # Date displayed if user hasn't made modifications.
                rx.skeleton(
                    text(
                        f"Submitted {report['time_ago']}",
                        class_name="text-sm italic",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
            ),
            class_name="flex-col flex-1 min-w-0 justify-center p-4"
        ),
        rx.flex(
            # Edit button.
            rx.flex(
                rx.skeleton(
                    rx.icon("pencil", class_name="h-5 w-5 stroke-zinc-700 dark:stroke-zinc-500"),
                    loading=~rx.State.is_hydrated,
                ),
                on_click=ReportState.edit_user_report(
                            report["report_id"], report["hospital_id"]
                ),
                class_name="flex-col items-center justify-center w-16 md:w-24 active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer"
            ),
        ),
        class_name="flex-row justify-between w-full"
    )


def report_item_dashboard_remove_report(report: dict[str, str]) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            flex(
                rx.skeleton(
                    outline_button(
                        rx.icon("trash-2", class_name="h-4 w-4"),
                    ),
                    loading=~rx.State.is_hydrated,
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
                        ),
                        outline_button(
                            "Cancel",
                        ),
                        class_name="flex-col space-y-4 w-full",
                    )
                ),
                class_name="flex-col items-center space-y-4",
            )
        ),
    )
