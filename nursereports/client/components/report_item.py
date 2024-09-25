
from ...states import DashboardState, ReportState

import reflex as rx


def report_item_dashboard(report: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.cond(
                        report["assign_select_unit"],
                        rx.cond(
                            report["assign_select_unit"] == "I don't see my unit",
                            rx.text(
                                f"{report['assign_input_unit_name']}",
                                font_weight="bold",
                                font_size=["16px", "16px", "18px", "18px", "18px"],
                                line_height="1em",
                            ),
                            rx.text(
                                f"{report['assign_select_unit']}",
                                font_weight="bold",
                                font_size=["16px", "16px", "18px", "18px", "18px"],
                                line_height="1em",
                            ),
                        ),
                        rx.cond(
                            report['assign_select_area']
                            == "I don't see my area or role",
                            rx.text(
                                f"{report['assign_input_area']}",
                                font_weight="bold",
                                font_size=["16px", "16px", "18px", "18px", "18px"],
                                line_height="1em",
                            ),
                            rx.text(
                                f"{report['assign_select_area']}",
                                font_weight="bold",
                                font_size=["16px", "16px", "18px", "18px", "18px"],
                                line_height="1em",
                            ),
                        ),
                    ),
                    rx.cond(
                        report["modified_at"],
                        rx.text(
                            f"Edited {report['modified_at']}",
                            font_size="14px",
                            font_style="italic",
                        ),
                        rx.text(
                            f"Submitted {report['created_at']}",
                            font_size="14px",
                            font_style="italic",
                        ),
                    ),
                    width="100%",
                    flex_direction="column",
                    gap=["4px", "4px", "12px", "12px", "12px"],
                ),
                align="center",
                margin="24px",
            ),
            rx.spacer(),
            rx.flex(
                report_item_dashboard_ellipsis(report),
                align="center",
                justify="center",
                height="100%",
                min_height="100px",
                width="100px",
                min_width="100px",
            ),
            rx.flex(
                report_item_dashboard_edit(report),
                align="center",
                justify="center",
                height="100%",
                min_height="100px",
                width="100px",
                min_width="100px",
                border_left="1px solid var(--chakra-colors-chakra-border-color)",
            ),
            flex_direction="row",
            width="100%",
        ),
        min_height="100px",
        width="100%"
    )


def report_item_dashboard_ellipsis(report: dict[str, str]) -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon("ellipsis-vertical"),
                height="36px",
                width="36px",
                variant="ghost",
                cursor="pointer"
            )
        ),
        rx.menu.content(
            rx.menu.item(
                "Delete Report",
                on_click=[
                    DashboardState.set_report_to_remove(report['report_id']),
                    DashboardState.set_remove_report_confirmation_open(True)
                ]
            )
        )
    )


def report_item_dashboard_edit(report: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.button(
            rx.icon("pencil"),
            height="36px",
            width="36px",
            variant="ghost",
            cursor="pointer",
            on_click=ReportState.event_state_edit_user_report(report['report_id'])
        )
    )
