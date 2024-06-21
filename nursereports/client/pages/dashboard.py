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
        saved_hospitals(),
        spacer(height="48px"),
        trending_hospitals(),
        spacer(height="48px"),
        average_pay(),
        spacer(height="48px"),
        your_reviews(),
        spacer(height="48px"),
        width="100%",
        align="center",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def saved_hospitals() -> rx.Component:
    return rx.cond(
        BaseState.user_has_saved_hospitals, has_saved_hospitals(), no_saved_hospitals()
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
        max_width="1100px",
        padding_x="24px",
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
        max_width="1100px",
        padding_x="24px",
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
        max_width="1100px",
        padding_x="24px",
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
        padding_x="24px",
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
        padding_x="24px",
    )
