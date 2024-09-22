
from ..components import (
    c2a,
    footer,
    login_protected,
    navbar,
)
from ...states import BaseState

import reflex as rx

@rx.page(
    route="/hospital/[hosp_id]",
    title="Nurse Reports",
    on_load=BaseState.event_state_standard_flow("login"),
)
@login_protected
def hospital_overview() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        flex_direction='column',
        align_items='center',
        min_height='100vh'
    )

def content() -> rx.Component:
    return rx.flex(
        heading(),
        pay(),
        units(),
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def heading() -> rx.Component:
    return rx.flex(
        rx.text("Hospital heading")
    )

def pay() -> rx.Component:
    return rx.flex(
        pay_hospital(),
        pay_state()
    )

def pay_hospital() -> rx.Component:
    return rx.flex(
        rx.text("Hospital pay")
    )

def pay_state() -> rx.Component:
    return rx.flex(
        rx.text("State pay")
    )

def units() -> rx.Component:
    return rx.flex(
        rx.text("Hospital units")
    )

def unit_ratings() -> rx.Component:
    return rx.flex(
        rx.text("Unit ratings")
    )

def responses() -> rx.Component:
    return rx.flex(
        rx.text("Hospital responses")
    )