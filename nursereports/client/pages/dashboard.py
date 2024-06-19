from ..components.c2a import c2a
from ..components.custom import report_protected
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
        flex_direction="column",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        saved_hospitals(),
        trending_hospitals(),
        average_pay(),
        your_reviews(),
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
    return rx.flex()


def has_saved_hospitals() -> rx.Component:
    return rx.flex()


def trending_hospitals() -> rx.Component:
    return rx.flex()


def average_pay() -> rx.Component:
    return rx.flex()


def your_reviews() -> rx.Component:
    return rx.flex()
