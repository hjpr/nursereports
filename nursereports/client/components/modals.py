
from ...states import DashboardState

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
                    align="center"
                ),
                rx.separator(),
                rx.flex(
                    content,
                    width="100%"
                ),
                rx.flex(
                    rx.button(
                        "Close",
                        on_click=DashboardState.close_all_modals
                    ),
                    width="100%",
                    align="center",
                    justify="center"
                ),
                width="100%",
                spacing="4"
            ),
            flex_direction="column",
            width="100%",
        )
    )


def saved_hospitals_modal_content() -> rx.Component:
    return rx.flex(
        rx.text("Spectacles, testicles, wallet and watch.")
    )


def my_pay_modal_content() -> rx.Component:
    return rx.flex(
        rx.text("Shidding and farding.")
    )


def my_reports_modal_content() -> rx.Component:
    return rx.flex(
        rx.text("Tony'd had schizophrenia before - and this was not it.")
    )