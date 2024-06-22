from ..components.c2a import c2a
from ..components.custom import report_protected, spacer
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base_state import BaseState

import reflex as rx


@rx.page(
    route="/dashboard",
    title="Nurse Reports",
    on_load=BaseState.event_state_standard_flow("report"),
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
        spacer(height="48px"),
        dashboard_header(),
        spacer(height="36px"),
        hospitals_header(),
        spacer(height="12px"),
        hospitals(),
        spacer(height="36px"),
        average_pay_header(),
        spacer(height="12px"),
        average_pay(),
        spacer(height="36px"),
        your_reviews_header(),
        spacer(height="12px"),
        your_reviews(),
        spacer(height="36px"),
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
        rx.heading(
            "Dashboard",
            size="8",
            color_scheme="teal"
        ),
        width="100%",
        justify="center",
    )


def hospitals_header() -> rx.Component:
    return rx.flex(
        rx.heading(
            "My Hospitals",
            size="6",
            align="left",
            color_scheme="teal"
        ),
        width="100%",
    )


def hospitals() -> rx.Component:
    return rx.flex(
        rx.cond(
            BaseState.user_has_saved_hospitals, has_saved_hospitals(), no_saved_hospitals()
        ),
        trending_hospitals(),
        width="100%",
        align="center",
        flex_direction=["column", "column", "row", "row", "row"],
    )


def has_saved_hospitals() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Saved hospitals...", font_size='10px'),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center"
        ),
        height="300px",
        width="100%",
    )


def no_saved_hospitals() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("No saved hospitals...", font_size='10px'),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center"
        ),
        height="300px",
        width="100%",
        margin=[
            "0px 0px 24px 0px",
            "0px 0px 24px 0px",
            "0px 24px 0px 0px",
            "0px 24px 0px 0px",
            "0px 24px 0px 0px",
            ]
    )


def trending_hospitals() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Trending hospitals...", font_size='10px'),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center"
        ),
        height="300px",
        width="100%",
    )


def average_pay_header() -> rx.Component:
    return rx.flex(
        rx.heading(
            "My Pay Demographics",
            size="6",
            align="left",
            color_scheme="teal"
        ),
        width="100%",
    ) 


def average_pay() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Average pay in your area...", font_size='10px'),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center"
        ),
        height="300px",
        width="100%",
        max_width="1100px",
    )


def your_reviews_header() -> rx.Component:
    return rx.flex(
        rx.heading(
            "My Reviews",
            size="6",
            align="left",
            color_scheme="teal"
        ),
        width="100%",
    )


def your_reviews() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Your reviews...", font_size='10px'),
            height="100%",
            width="100%",
            align_items="center",
            justify_content="center"
        ),
        height="300px",
        width="100%",
        max_width="1100px",
    )
