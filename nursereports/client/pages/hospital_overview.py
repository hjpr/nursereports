
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
        HospitalState.event_state_load_review_info
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
            padding="24px",
            align="center",
            spacing="5",
            flex_direction="column",
            flex_basis="auto",
            flex_grow="1",
            flex_shrink="0",
        ),
        rx.flex(
            rx.spinner(),
            width="100%",
            max_width="1100px",
            padding="48px",
            align="center",
            justify="center"
        )
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
                HospitalState.units_areas_roles_for_units,
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
        rx.flex(
            # Reviews header.
            rx.flex(    
                rx.icon("speech", margin="4px 0 0 0"),
                rx.heading("Reviews", margin="0 0 0 12px"),
                width=["100%", "100%", "100%", "20%", "20%"],
                flex_direction="row",
                justify_content=["center", "center", "center", "flex-start", "flex-start"],
            ),
            rx.flex(
                height='24px',
                display=["flex", "flex", "flex", "none", "none"]
            ),
            # Container for reviews.
            rx.flex(
                rx.cond(
                    HospitalState.review_info,
                    # If hospital has reviews...
                    rx.flex(
                        rx.flex(
                            rx.cond(
                                HospitalState.units_areas_roles_for_reviews,
                                # If units and filters are available
                                rx.flex(
                                    rx.select(
                                        HospitalState.units_areas_roles_for_reviews,
                                        value=HospitalState.review_filter_units_areas_roles,
                                        placeholder="All units/areas/roles",
                                        label="Select a unit/area/role",
                                        on_change=HospitalState.set_review_filter_units_areas_roles
                                    ),
                                    rx.select(
                                        ["Most Recent", "Most Helpful"],
                                        value=HospitalState.review_sorted,
                                        placeholder="Sort by",
                                        label="Select a sort method",
                                        on_change=HospitalState.set_review_sorted
                                    ),
                                    rx.button(
                                        rx.text("Clear filters"),
                                        on_click=[
                                            HospitalState.set_review_filter_units_areas_roles(""),
                                            HospitalState.set_review_sorted("")
                                        ]
                                    ),
                                    flex_direction="row",
                                    flex_wrap="wrap",
                                    spacing="2",
                                    justify="center",
                                    width="100%"
                                ),
                                # If units and filters aren't available
                                rx.flex(
                                    rx.select(
                                        [],
                                        placeholder="No units/areas/roles",
                                        disabled=True
                                    ),
                                    rx.select(
                                        [],
                                        placeholder="No sorting available",
                                        disabled=True
                                    ),
                                    rx.button(
                                        "Clear filters",
                                    ),
                                    flex_direction="row",
                                    flex_wrap="wrap",
                                    spacing="2",
                                    justify="center",
                                    width="100%"
                                )
                            ),
                            justify="center",
                            padding="24px",
                            width="100%"
                        ),
                        rx.foreach(
                            HospitalState.filtered_review_info,
                            response_card
                        ),
                        flex_direction="column",
                        spacing="8"
                    ),
                    # If hospital doesn't have reviews...
                    rx.flex(
                        rx.text("Nothing yet, check back later!"),
                        justify="center",
                        width="100%"
                    )
                ),
                spacing='3',
                width="100%"
            ),
            flex_direction=["column", "column", "column", "row", "row"],
            width="100%",
        ),
        padding="24px 0 0 0",
        width="100%"
    )

def response_card(review: dict[str, str]) -> rx.Component:
    """
    Renders the review card for the hospital overview.

    Dict:
        user_id
        created_at
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
                    rx.text(review["formatted_created_at"]),
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
            rx.flex(
                rx.cond(
                    review["user_has_liked"],
                    # If user has liked the review
                    rx.flex(
                        rx.button(
                            rx.icon("thumbs-up", size=18),
                            rx.text(review["likes_number"]),
                            variant="ghost",
                            cursor="pointer",
                            _hover={"bg": "none"},
                            on_click=HospitalState.event_state_like_unlike_review(review)
                        ),
                        rx.text("You upvoted this.", size="2"),
                        flex_direction="column",
                        spacing="2"
                    ),
                    # If user hasn't liked review
                    rx.flex(
                        rx.button(
                            rx.icon("thumbs-up", size=18),
                            rx.text(review["likes_number"]),
                            variant="ghost",
                            cursor="pointer",
                            _hover={"bg": "none"},
                            on_click=HospitalState.event_state_like_unlike_review(review)
                        )
                    )
                ),
                align="center",
                justify="center",
                spacing="1",
                flex_direction="row",
                width="100%"
            ),
            width="100%",
        ),
        width="100%"
    )