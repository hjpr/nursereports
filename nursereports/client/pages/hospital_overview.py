
from ..components import (
    c2a,
    footer,
    report_protected,
    navbar,
)
from ...states import BaseState, HospitalState

import reflex as rx

@rx.page(
    route="/hospital/[hosp_id]",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_standard_flow("login"),
        HospitalState.event_state_load_hospital_info,
    ]

)
@report_protected
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
    return rx.cond(
        BaseState.is_hydrated,
        rx.flex(
            heading(),
            pay(),
            units(),
            responses(),
            width="100%",
            max_width="1100px",
            padding="48px",
            align="center",
            spacing="5",
            flex_direction="column",
            flex_basis="auto",
            flex_grow="1",
            flex_shrink="0",
        ),
        rx.spinner()
    )

def heading() -> rx.Component:
    return rx.cond(
        HospitalState.cms_id,
        rx.flex(
            rx.flex(
                rx.heading(HospitalState.hospital_info["hosp_name"]),
                rx.text(HospitalState.hospital_info["hosp_address"]),
                rx.text(
                    f"{HospitalState.hospital_info["hosp_city"]}, {HospitalState.hospital_info["hosp_state"]} {HospitalState.hospital_info["hosp_zip"]}"
                ),
                flex_direction="column",
                spacing='2'
            ),
            height="100%",
            width="100%",
            padding="24px",
            justify="center"
        ),
        rx.card(
            rx.text("No hospital information."),
            height="100%",
            width="100%",
            padding="24px"
        )
    )

def pay() -> rx.Component:
    return rx.card(
        rx.flex(
            pay_hospital(),
            pay_state(),
            flex_direction="row",
            spacing='2',
            height="100%",
            width="100%"
        ),
        height="100%",
        width="100%",
        padding="24px",   
    )

def pay_hospital() -> rx.Component:
    return rx.flex(
        rx.text("Hospital pay placeholder"),
        justify="center",
        width="100%"
    )

def pay_state() -> rx.Component:
    return rx.flex(
        rx.text("State pay placeholder"),
        justify="center",
        width="100%"
    )

def units() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Hospital units placeholder"),
            justify="center",
            height="100%",
            width="100%"
        ),
        height="100%",
        width="100%",
        padding="24px"
    )

def unit_ratings() -> rx.Component:
    return rx.flex(
        rx.text("Unit ratings")
    )

def responses() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text("Hospital responses placeholder"),
            justify='center',
            height="100%",
            width='100%'
        ),
        height="100%",
        width="100%",
        padding="24px"
    )