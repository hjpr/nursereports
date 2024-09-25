
from ..components import (
    c2a,
    footer,
    report_protected,
    navbar,
)
from ...states import BaseState, HospitalState

import reflex as rx

@rx.page(
    route="/hospital/[cms_id]",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_standard_flow("report"),
        HospitalState.event_state_load_hospital_info,
        HospitalState.event_state_load_report_info,
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
            rx.divider(),
            pay(),
            rx.divider(),
            units(),
            rx.divider(),
            reviews(),
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
        HospitalState.hosp_id,
        rx.flex(
            rx.flex(
                rx.heading(HospitalState.hospital_info["hosp_name"], size='7'),
                rx.text(HospitalState.hospital_info["hosp_address"]),
                rx.text(f'{HospitalState.hospital_info["hosp_city"]}, {HospitalState.hospital_info["hosp_state"]} {HospitalState.hospital_info["hosp_zip"]}'),
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
    return rx.flex(
        rx.hstack(
            rx.flex(
                rx.icon("piggy-bank"),
                rx.heading("Pay", padding="0px 12px"),
                width="20%",
                flex_direction="row",
                align="center",
            ),
            pay_hospital(),
            pay_state(),
            spacing='2',
            height="100%",
            width="100%"
        ),
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
    """Units section."""
    return rx.flex(
        rx.hstack(
            # Units header.
            rx.flex(
                rx.icon("stethoscope"),
                rx.heading("Units", padding="0px 12px"),
                width="20%",
                flex_direction="row",
                align="center",
            ),
            # Container for units.
            rx.cond(
                HospitalState.unit_area_role_info,
                # If reviews for units present...
                rx.flex(
                    unit_ratings_graph(),
                    unit_grades(),
                    justify="center",
                    width="100%"
                ),
                # If reviews for units not present...
                rx.flex(
                    rx.text("Nothing yet, check back later!"),
                    justify="center",
                    width="100%"
                )
            ),
            width="100%"
        ),
        width="100%",
        padding="24px"
    )

def unit_ratings_graph() -> rx.Component:
    return rx.flex(
        rx.text("Unit Ratings Graph Placeholder."),
        width="100%"
    )

def unit_grades() -> rx.Component:
    return rx.flex(
        rx.text("Unit Grades Placeholder."),
        width="100%"
    )

def reviews() -> rx.Component:
    """Free response section."""
    return rx.flex(
        rx.hstack(
            # Reviews header.
            rx.flex(
                rx.icon("speech"),
                rx.heading("Reviews", padding="0px 12px"),
                width="20%",
                flex_direction="row",
                align="center",
            ),
            # Container for reviews.
            rx.flex(
                rx.cond(
                    HospitalState.review_info,
                    # If hospital has reviews...
                    rx.vstack(
                        rx.foreach(
                            HospitalState.review_info,
                            response_card
                        )
                    ),
                    # If hospital doesn't have reviews...
                    rx.flex(
                        rx.text("Nothing yet, check back later!"),
                        justify="center",
                        width="100%"
                    )
                ),
                width="100%"
            ),
            width="100%"
        ),
        width="100%",
        padding="24px"
    )

def response_card(review: dict[str, str]) -> rx.Component:
    """
    Renders the review card for the hospital overview.

    Dict:
        user_id
        has_comp_comments
        comp_comments
        has_assign_comments
        assign_comments
        has_staffing_comments
        staffing_comments
        has_unit
        unit
        has_area_role
        area_role
    """
    return rx.flex(
        rx.vstack(
            rx.hstack(
                rx.cond(
                    review["has_unit"],    
                    rx.text(review["unit"], weight="bold"),
                    rx.text(review["area_role"], weight="bold")
                ),
                rx.spacer(),
                rx.flex(
                    rx.button(
                        rx.icon("flag", color="red", size=18),
                        variant="ghost",
                        cursor="pointer",
                        margin="0 12px 0 0",
                        _hover={"bg": "none"}
                    ),
                    rx.button(
                        rx.icon("thumbs-up", size=18),
                        rx.text("0"),
                        variant="ghost",
                        cursor="pointer",
                        _hover={"bg": "none"}
                    ),
                    align="center",
                    spacing="1",
                    flex_direction="row"
                ),
                width="100%"
            ),
            rx.cond(
                review["has_comp_comments"],
                rx.flex(
                    rx.text(review["comp_comments"]),
                    width="100%"
                )
            ),
            rx.cond(
                review["has_assign_comments"],
                rx.flex(
                    rx.text(review["assign_comments"]),
                    width="100%"
                )
            ),
            rx.cond(
                review["has_staffing_comments"],
                rx.flex(
                    rx.text(review["staffing_comments"]),
                    width="100%"
                )
            ),
            width="100%",
        ),
        padding="24px",
        width="100%"
    )