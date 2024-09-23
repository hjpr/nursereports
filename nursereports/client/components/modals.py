from ...states import BaseState, DashboardState

import reflex as rx


def info_modal(title: str, content: rx.Component) -> rx.Component:
    """Embed this modal within rx.dialog.root"""
    return rx.dialog.content(
        rx.flex(
            rx.vstack(
                rx.flex(
                    rx.icon("info"),
                    rx.heading(f"{title}", padding="0 12px"),
                    width="100%",
                    align="center",
                ),
                rx.separator(),
                rx.flex(content, width="100%"),
                rx.flex(
                    rx.button("Close", on_click=DashboardState.close_all_modals),
                    width="100%",
                    align="center",
                    justify="center",
                ),
                width="100%",
                spacing="4",
            ),
            flex_direction="column",
            width="100%",
        )
    )


def saved_hospitals_modal_content() -> rx.Component:
    return rx.flex(
        rx.text("Save hospitals to your dashboard to keep a close eye on them.")
    )


def my_pay_modal_content() -> rx.Component:
    return rx.flex(
        rx.text("Compare local hospital rates to the state average.")
    )


def my_reports_modal_content() -> rx.Component:
    return rx.flex(
        rx.text("Review and edit all reports that you've made.")
    )


def remove_report_modal() -> rx.Component:
    """Embed this modal within rx.dialog.root"""
    return rx.dialog.content(
        rx.flex(
            rx.vstack(
                rx.flex(
                    rx.icon("octagon-alert", color="#E5484D"),
                    rx.heading("Confirm Delete Report", padding="0 12px"),
                    width="100%",
                    align="center",
                ),
                rx.separator(),
                rx.flex(
                    rx.text("""
                    You are about to completely delete this report. Our goal is to maintain
                    as many valid reports as possible. If appropriate, please consider
                    editing this report, or submitting a new report instead. Each entry is
                    valuable to your peers!
                    """
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.flex(
                        rx.button(
                            "Close",
                            variant="ghost",
                            _focus={"outline": "none"},
                            on_click=[
                                DashboardState.set_remove_report_confirmation_open(False),
                                DashboardState.set_report_to_remove("")
                            ]
                        ),
                        rx.button(
                            "Delete this Report",
                            color_scheme="red",
                            on_click=[
                                BaseState.event_state_remove_report(DashboardState.report_to_remove),
                                DashboardState.set_remove_report_confirmation_open(False),
                                DashboardState.set_report_to_remove("")
                            ]
                        ),
                        align="center",
                        spacing="9"
                    ),
                    width="100%",
                    align="center",
                    justify="center"
                ),
                width="100%",
                spacing="4",
            ),
            flex_direction="column",
            width="100%",
        )
    )
