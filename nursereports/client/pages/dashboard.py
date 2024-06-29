from ..components import (
    c2a,
    footer,
    hospital_item_dashboard,
    navbar,
    report_protected
)
from ...states.base_state import BaseState

import reflex as rx


@rx.page(
    route="/dashboard",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_standard_flow("report"),
        BaseState.event_state_refresh_user_info,
    ],
)
@report_protected
def dashboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        background="linear-gradient(ghostwhite, honeydew)",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        dashboard_header(),
        my_hospitals_header(),
        my_hospitals(),
        my_pay_header(),
        my_pay(),
        my_reviews_header(),
        my_reviews(),
        width="100%",
        max_width="1100px",
        padding="24px",
        align="center",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def dashboard_header() -> rx.Component:
    return rx.flex(
        rx.heading("My Dashboard", size="8", color_scheme="teal"),
        width="100%",
        justify="center",
        margin="36px 0px 72px 0px",
    )


def my_hospitals_header() -> rx.Component:
    return rx.flex(
        rx.heading("My Hospitals", size="6", align="left", color_scheme="teal"),
        width="100%",
        margin="0px 0px 12px 0px",
    )


def my_hospitals() -> rx.Component:
    return rx.card(
        rx.cond(
            BaseState.saved_hospitals,
            rx.flex(
                rx.foreach(BaseState.saved_hospitals, hospital_item_dashboard),
                height="100%",
                width="100%",
                flex_direction='column',
                spacing="3",
                align_items="center",
                justify_content="center",
            ),
            rx.flex(
                rx.text("You haven't saved any hospitals..."),
                rx.button(
                    "Test Add Hospital",
                    on_click=BaseState.update_user_info(
                        {"saved_hospitals": [12345, 67890]}
                    ),
                ),
                height="100%",
                width="100%",
                align_items="center",
                justify_content="center",
                flex_direction="column",
                spacing="3",
                padding="24px 24px 24px 24px",
            ),
        ),
        height="100%",
        width="100%",
        margin=["0px 0px 12px 0px"],
    )


def trending_hospitals() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Trending hospitals...", font_size="10px"),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center",
        ),
        height="300px",
        width="100%",
        margin=[
            "12px 0px 0px 0px",
            "12px 0px 0px 0px",
            "0px 0px 0px 12px",
            "0px 0px 0px 12px",
            "0px 0px 0px 12px",
        ],
    )


def my_pay_header() -> rx.Component:
    return rx.flex(
        rx.heading("My Pay Demographics", size="6", align="left", color_scheme="teal"),
        width="100%",
        margin="0px 0px 12px 0px",
    )


def my_pay() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Average pay in your area...", font_size="10px"),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center",
        ),
        height="300px",
        width="100%",
        max_width="1100px",
        margin="0px 0px 24px 0px",
    )


def my_reviews_header() -> rx.Component:
    return rx.flex(
        rx.heading("My Reviews", size="6", align="left", color_scheme="teal"),
        width="100%",
        margin="0px 0px 12px 0px",
    )


def my_reviews() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Your reviews...", font_size="10px"),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center",
        ),
        height="300px",
        width="100%",
        max_width="1100px",
        margin="0px 0px 24px 0px",
    )
