
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
        HospitalState.event_state_load_pay_info,
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
        class_name="flex-col items-center bg-teal-50 min-h-screen"
    ) 

def content() -> rx.Component:
    return rx.cond(
        BaseState.is_hydrated,
        rx.flex(
            heading(),
            pay(),
            units(),
            reviews(),
            class_name="space-y-3 divide-y",
            width="100%",
            max_width="1100px",
            align="center",
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
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("banknote", class_name="mr-3 h-8 w-8"),
                    rx.text("Pay", class_name="font-bold text-2xl"),
                    class_name="flex-row items-center"
                ),
                class_name="flex-col items-center lg:items-start w-full lg:w-3/12"
            ),
            rx.flex(
                rx.segmented_control.root(
                    rx.segmented_control.item("Staff", value="staff"),
                    rx.segmented_control.item("Travelers", value="contract"),
                    size="2",
                    on_change=HospitalState.setvar("selected_pay_tab"),
                    value=HospitalState.selected_pay_tab,
                    width="100%"
                ),
                pay_content(),
                class_name="flex-col items-center rounded shadow-lg bg-white md:justify-self-center space-y-6 md:space-y-10 p-6 lg:p-12 w-full"
            ),
            class_name="flex-col lg:flex-row space-y-6 lg:space-y-0 w-full"
        ),
        class_name="flex-row p-6 lg:p-12 w-full"
    )

def pay_content() -> rx.Component:
    return rx.cond(
        HospitalState.selected_pay_tab == "staff",
        # STAFF INFORMATION
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.match(
                        HospitalState.selected_employment_type,
                        ("Full-time", full_time_hospital_pay_card()),
                        ("Part-time", part_time_hospital_pay()),
                        ("PRN", prn_hospital_pay())
                    ),
                    class_name="flex-col items-center w-full"
                ),
                # STATE AVERAGE
                rx.flex(
                    rx.match(
                        HospitalState.selected_employment_type,
                        ("Full-time", full_time_state_pay_card()),
                        ("Part-time", part_time_state_pay()),
                        ("PRN", prn_state_pay())
                    ),
                    class_name="flex-col items-center w-full"
                ),
                class_name="flex-col md:flex-row justify-center divide-y md:divide-y-0 md:divide-x w-full"
            ),
            staff_experience_control_slider(),
            staff_employment_type_selection(),
            class_name="flex-col border rounded divide-y w-full"
        ),
        # TRAVELER INFORMATION
        rx.flex(
            rx.card(
                rx.text("Hospital Travel Pay")
            ),
            rx.card(
                rx.text("State Travel Pay")
            ),
            class_name="flex-col md:flex-row w-full"
        )
    )

def full_time_hospital_pay_card() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "Hospital Estimate",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.cond(
                HospitalState.interpolated_ft_pay_hospital,
                rx.flex(
                    rx.text(
                        HospitalState.ft_pay_hospital_formatted["hourly"],
                        class_name="text-3xl font-bold"
                    ),
                    rx.text(
                        HospitalState.ft_pay_hospital_formatted["yearly"],
                        class_name="text-lg"
                    ),
                    class_name="flex-col items-center justify-center w-full"
                ),
                rx.flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center w-full"
                )
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            rx.flex(
                rx.cond(
                    HospitalState.ft_pay_hospital_info_limited & HospitalState.interpolated_ft_pay_hospital,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                rx.cond(
                    ~HospitalState.interpolated_ft_pay_hospital,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="red",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def full_time_state_pay_card() -> rx.Component:
    return rx.flex(
        # HEADER
        rx.flex(
            rx.text(
                "State Average",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        # STATE PAY INFO
        rx.flex(
            rx.cond(
                HospitalState.interpolated_ft_pay_state,
                rx.flex(
                    rx.text(
                        HospitalState.ft_pay_state_formatted,
                        class_name="text-4xl font-bold"
                    ),
                    class_name="flex-col items-center justify-center w-full"
                ),
                rx.flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center w-full"
                )
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            # Callouts
            rx.flex(
                rx.cond(
                    HospitalState.ft_pay_state_info_limited & HospitalState.interpolated_ft_pay_state,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                rx.cond(
                    ~HospitalState.interpolated_ft_pay_state,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="red",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def part_time_hospital_pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "Hospital Estimate",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.cond(
                HospitalState.interpolated_pt_pay_hospital,
                rx.flex(
                    rx.text(
                        HospitalState.pt_pay_hospital_formatted,
                        class_name="text-4xl font-bold"
                    ),
                    class_name="flex-col items-center justify-center w-full"
                ),
                rx.flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center w-full"
                )
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            rx.flex(
                rx.cond(
                    HospitalState.ft_pay_hospital_info_limited & HospitalState.interpolated_pt_pay_hospital,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                rx.cond(
                    ~HospitalState.interpolated_pt_pay_hospital,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="red",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )


def part_time_state_pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "State Average",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.cond(
                HospitalState.interpolated_pt_pay_state,
                rx.flex(
                    rx.text(
                        HospitalState.pt_pay_state_formatted,
                        class_name="text-4xl font-bold"
                    ),
                    class_name="flex-col items-center justify-center w-full"
                ),
                rx.flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center w-full"
                )
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            rx.flex(
                rx.cond(
                    HospitalState.pt_pay_state_info_limited & HospitalState.interpolated_pt_pay_state,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                rx.cond(
                    ~HospitalState.interpolated_pt_pay_state,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="red",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def prn_hospital_pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "Hospital Estimate",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.cond(
                HospitalState.interpolated_prn_pay_hospital,
                rx.flex(
                    rx.text(
                        HospitalState.prn_pay_hospital_formatted,
                        class_name="text-4xl font-bold"
                    ),
                    class_name="flex-col items-center justify-center w-full"
                ),
                rx.flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center w-full"
                )
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            rx.flex(
                rx.cond(
                    HospitalState.prn_pay_hospital_info_limited & HospitalState.interpolated_prn_pay_hospital,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                rx.cond(
                    ~HospitalState.interpolated_prn_pay_hospital,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="red",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def prn_state_pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "State Average",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.cond(
                HospitalState.interpolated_prn_pay_state,
                rx.flex(
                    rx.text(
                        HospitalState.prn_pay_state_formatted,
                        class_name="text-4xl font-bold"
                    ),
                    class_name="flex-col items-center justify-center w-full"
                ),
                rx.flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center w-full"
                )
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            rx.flex(
                rx.cond(
                    HospitalState.prn_pay_state_info_limited & HospitalState.interpolated_prn_pay_state,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                rx.cond(
                    ~HospitalState.interpolated_prn_pay_state,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="red",
                        variant="surface",
                        class_name="w-auto"
                    ),
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def contract_hospital_pay() -> rx.Component:
    return rx.flex()

def contract_state_pay() -> rx.Component:
    return rx.flex()

def staff_experience_control_slider() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "Experience",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.text(
                f"{HospitalState.selected_experience} year(s)",
                class_name="text-xl font-bold"
            ),
            rx.slider(
                default_value=HospitalState.selected_experience,
                min=0,
                max=26,
                on_change=HospitalState.set_slider,
                class_name="p-4"
            ),
            rx.text(
                "Set slider to view rates by experience",
                class_name="italic"
            ),
            class_name="flex-col items-center p-6 space-y-2 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def staff_employment_type_selection() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                "Employment Type",
                class_name="text-xl"
            ),
            class_name="flex-col bg-teal-100 items-center p-3 w-full"
        ),
        rx.flex(
            rx.radio(
                ["Full-time", "Part-time", "PRN"],
                direction="row",
                size="3",
                spacing="3",
                value=HospitalState.selected_employment_type,
                on_change=HospitalState.setvar("selected_employment_type"),
            ),
            rx.text(
                "Select to view pay for that employment type",
                class_name="italic"
            ),
            class_name="flex-col items-center space-y-4 p-6 w-full"
        ),
        class_name="flex-col items-center divide-y divide-dashed w-full"
    )

def units() -> rx.Component:
    """Units section."""
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.icon("stethoscope", margin="4px 0 0 0"),
                rx.heading("Units", padding="0px 12px"),
                width=["100%", "100%", "100%", "20%", "20%"],
                flex_direction="row",
                justify_content=["center", "center", "center", "flex-start", "flex-start"],
            ),
            rx.flex(
                height="24px",
                display=["flex", "flex", "flex", "none", "none"]

            ),
            # Container for units.
            rx.cond(
                HospitalState.units_areas_roles_for_units,
                # If reviews for units present...
                rx.flex(
                    unit_grades(),
                    unit_ratings_graph(),
                    justify="center",
                    padding="24px",
                    width="100%"
                ),
                # If reviews for units not present...
                rx.flex(
                    rx.text("Nothing yet, check back later!"),
                    justify="center",
                    padding="24px",
                    width="100%"
                )
            ),
            flex_direction=["column", "column", "column", "row", "row"],
            width="100%",
        ),
        width="100%",
        padding="24px 0 24px 0"
    )

def unit_grades() -> rx.Component:
    return rx.flex(
        rx.text("Unit Grades Placeholder."),
        width="100%"
    )

def unit_ratings_graph() -> rx.Component:
    return rx.flex(
        rx.text("Unit Ratings Graph Placeholder."),
        width="100%"
    )

def reviews() -> rx.Component:
    """Free response section."""
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(    
                    rx.icon("speech", class_name="mr-3 h-8 w-8"),
                    rx.heading("Reviews", class_name="font-bold text-2xl"),
                    class_name="flex-row items-center"
                ),
                class_name="flex-col items-center lg:items-start w-full lg:w-3/12"
            ),
            rx.flex(
                review_content(),
                class_name="flex-col items-center rounded shadow-lg bg-white md:justify-self-center space-y-6 md:space-y-10 p-6 lg:p-12 w-full"
            ),
            class_name="flex-col lg:flex-row space-y-6 lg:space-y-0 w-full"
        ),
        class_name="flex-row p-6 lg:p-12 w-full"
    )

def review_content() -> rx.Component:
    return rx.flex(
        rx.cond(
            HospitalState.review_info,
            # REVIEWS PRESENT
            rx.flex(
                rx.cond(
                    HospitalState.units_areas_roles_for_reviews,
                    review_filters(),
                ),
                rx.flex(
                    rx.foreach(
                        HospitalState.filtered_review_info,
                        response_card,
                    ),
                    class_name="flex-col divide-y w-full"
                ),
                class_name="flex-col space-y-3 w-full"
            ),
            # REVIEWS NOT PRESENT
            rx.flex(
                rx.text("Nothing yet, check back later!"),
                class_name="flex-col items-center p-6 w-full"
            ),
        ),
        class_name="flex-col items-center w-full"
    )

def review_filters() -> rx.Component:
    return rx.flex(
        rx.select(
            HospitalState.units_areas_roles_for_reviews,
            value=HospitalState.review_filter_units_areas_roles,
            placeholder="All units/areas/roles",
            label="Select a unit/area/role",
            size="2",
            on_change=HospitalState.set_review_filter_units_areas_roles,
            width=["50%", "50%", "auto", "auto", "auto"]
        ),
        rx.select(
            ["Most Recent", "Most Helpful"],
            value=HospitalState.review_sorted,
            placeholder="Sort by",
            label="Select a sort method",
            size="2",
            on_change=HospitalState.set_review_sorted,
            width=["50%", "50%", "auto", "auto", "auto"]
        ),
        rx.button(
            rx.text("Clear filters"),
            size="2",
            on_click=[
                HospitalState.set_review_filter_units_areas_roles(""),
                HospitalState.set_review_sorted("")
            ],
            width=["50%", "50%", "auto", "auto", "auto"]
        ),
        class_name="flex-col md:flex-row items-center md:justify-center space-y-2 md:space-y-0 md:space-x-2 w-full"
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
                        rx.text(" - You upvoted.", class_name="text-sm text-teal-600 pl-1"),
                        class_name="flex-row items-center"
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
                class_name="flex-row items-center justify-center w-full"
            ),
            class_name="w-full"
        ),
        class_name="py-6 w-full"
    )