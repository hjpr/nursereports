from ..components import (
    c2a,
    flex,
    footer,
    report_protected,
    navbar,
    solid_button,
    outline_button,
    text
)
from ...states import (
    BaseState,
    HospitalState,
    ReportState
)

import reflex as rx


@rx.page(
    route="/hospital/[cms_id]",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("report"),
        HospitalState.event_state_load_hospital_info,
        HospitalState.event_state_load_report_info,
        HospitalState.event_state_load_pay_info,
        HospitalState.event_state_load_unit_info,
        HospitalState.event_state_load_review_info,
    ],
)
@report_protected
def hospital_overview() -> rx.Component:
    return flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-teal-300",
    )


def content() -> rx.Component:
    return flex(
            heading(),
            pay(),
            units(),
            reviews(),
            class_name="flex-col items-center space-y-8 px-4 py-8 w-full max-w-screen-md",
    )


def heading() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("hospital", class_name="h-6 w-6 stroke-zinc-700 dark:stroke-teal-800"),
                text("Hospital Overview", class_name="text-2xl font-bold"),
                class_name="flex-row items-center space-x-2"
            ),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-4 w-full"
        ),
        rx.flex(
            heading_content(),
            class_name="w-full"
        ),
        rx.flex(
            heading_buttons(),
            class_name="w-full"
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )


def heading_content() -> rx.Component:
    return flex(
        flex(
            rx.skeleton(
                rx.text(HospitalState.hospital_info["hosp_name"], class_name="font-bold text-center text-2xl"),
                loading=~rx.State.is_hydrated
            ),
            rx.skeleton(
                rx.text(HospitalState.hospital_info["hosp_addr"], class_name="italic text-sm"),
                loading=~rx.State.is_hydrated
                ),
            rx.skeleton(
                rx.text(
                    f'{HospitalState.hospital_info["hosp_city"]}, {HospitalState.hospital_info["hosp_state"]} {HospitalState.hospital_info["hosp_zip"]}',
                    class_name="italic text-sm"
                ),
                loading=~rx.State.is_hydrated
            ),
            class_name="flex-col items-center space-y-1 w-full",
        ),
        class_name="p-4 w-full"
    )


def heading_buttons() -> rx.Component:
    return rx.flex(
        solid_button(
            "Submit Full Report",
            class_name="w-full md:w-auto",
            on_click=ReportState.event_state_create_full_report(HospitalState.hosp_id)
        ),
        outline_button(
            "Submit Pay Report",
            class_name="w-full md:w-auto"
        ),
        outline_button(
            "Request Page Moderation",
            class_name="w-full md:w-auto"
        ),
        class_name="flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 items-center justify-center p-4 w-full"
    )


def pay() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("banknote", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Pay", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
        class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        flex(
            rx.segmented_control.root(
                rx.segmented_control.item("Staff", value="staff"),
                rx.segmented_control.item("Travelers", value="contract"),
                size="2",
                on_change=HospitalState.setvar("selected_pay_tab"),
                value=HospitalState.selected_pay_tab,
            ),
            pay_content(),
            class_name="flex-col items-center p-4 space-y-4 w-full",
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )


def pay_content() -> rx.Component:
    return rx.cond(
        HospitalState.selected_pay_tab == "staff",
        # STAFF INFORMATION
        flex(
            flex(
                flex(
                    rx.match(
                        HospitalState.selected_employment_type,
                        ("Full-time", full_time_hospital_pay_card()),
                        ("Part-time", part_time_hospital_pay()),
                    ),
                    class_name="flex-col items-center w-full",
                ),
                # STATE AVERAGE
                flex(
                    rx.match(
                        HospitalState.selected_employment_type,
                        ("Full-time", full_time_state_pay_card()),
                        ("Part-time", part_time_state_pay()),
                    ),
                    class_name="flex-col items-center w-full",
                ),
                class_name="flex-col md:flex-row justify-center divide-y md:divide-y-0 md:divide-x w-full",
            ),
            staff_experience_control_slider(),
            staff_employment_type_selection(),
            class_name="flex-col border rounded divide-y w-full",
        ),
        # TRAVELER INFORMATION
        flex(
            rx.card(rx.text("Hospital Travel Pay")),
            rx.card(rx.text("State Travel Pay")),
            class_name="flex-col md:flex-row w-full",
        ),
    )


def full_time_hospital_pay_card() -> rx.Component:
    return flex(
        flex(
            rx.text("Hospital Average", class_name="text-xl font-bold"),
            class_name="flex-col bg-teal-100 items-center p-2 w-full",
        ),
        flex(
            rx.cond(
                HospitalState.extrapolated_ft_pay_hospital,
                flex(
                    rx.text(
                        HospitalState.ft_pay_hospital_formatted["hourly"],
                        class_name="text-3xl font-bold",
                    ),
                    rx.text(
                        HospitalState.ft_pay_hospital_formatted["yearly"],
                        class_name="text-lg",
                    ),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
                flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            flex(
                rx.cond(
                    HospitalState.ft_pay_hospital_info_limited
                    & HospitalState.extrapolated_ft_pay_hospital,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                rx.cond(
                    ~HospitalState.extrapolated_ft_pay_hospital,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="ruby",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                class_name="flex-col items-center w-full",
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full",
        ),
        class_name="flex-col items-center divide-y w-full",
    )


def full_time_state_pay_card() -> rx.Component:
    return flex(
        # HEADER
        flex(
            rx.text("State Average", class_name="text-xl font-bold"),
            class_name="flex-col bg-teal-100 items-center p-2 w-full",
        ),
        # STATE PAY INFO
        flex(
            rx.cond(
                HospitalState.extrapolated_ft_pay_state,
                flex(
                    rx.text(
                        HospitalState.ft_pay_state_formatted,
                        class_name="text-4xl font-bold",
                    ),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
                flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            # Callouts
            flex(
                rx.cond(
                    HospitalState.ft_pay_state_info_limited
                    & HospitalState.extrapolated_ft_pay_state,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                rx.cond(
                    ~HospitalState.extrapolated_ft_pay_state,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="ruby",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                class_name="flex-col items-center w-full",
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full",
        ),
        class_name="flex-col items-center divide-y w-full",
    )


def part_time_hospital_pay() -> rx.Component:
    return flex(
        flex(
            rx.text("Hospital Average", class_name="text-xl font-bold"),
            class_name="flex-col bg-teal-100 items-center p-2 w-full",
        ),
        flex(
            rx.cond(
                HospitalState.extrapolated_pt_pay_hospital,
                flex(
                    rx.text(
                        HospitalState.pt_pay_hospital_formatted,
                        class_name="text-4xl font-bold",
                    ),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
                flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            flex(
                rx.cond(
                    HospitalState.ft_pay_hospital_info_limited
                    & HospitalState.extrapolated_pt_pay_hospital,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                rx.cond(
                    ~HospitalState.extrapolated_pt_pay_hospital,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="ruby",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                class_name="flex-col items-center w-full",
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full",
        ),
        class_name="flex-col items-center divide-y w-full",
    )


def part_time_state_pay() -> rx.Component:
    return flex(
        flex(
            rx.text("State Average", class_name="text-xl font-bold"),
            class_name="flex-col bg-teal-100 items-center p-2 w-full",
        ),
        flex(
            rx.cond(
                HospitalState.extrapolated_pt_pay_state,
                flex(
                    rx.text(
                        HospitalState.pt_pay_state_formatted,
                        class_name="text-4xl font-bold",
                    ),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
                flex(
                    rx.icon("ban", color="lightgrey", size=40),
                    class_name="flex-col items-center justify-center h-14 w-full",
                ),
            ),
            rx.badge(HospitalState.selected_employment_type, size="3"),
            flex(
                rx.cond(
                    HospitalState.pt_pay_state_info_limited
                    & HospitalState.extrapolated_pt_pay_state,
                    rx.callout(
                        "Limited pay data",
                        icon="triangle_alert",
                        color_scheme="orange",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                rx.cond(
                    ~HospitalState.extrapolated_pt_pay_state,
                    rx.callout(
                        "No pay data",
                        icon="octagon_alert",
                        color_scheme="ruby",
                        variant="surface",
                        size="1",
                        class_name="w-auto",
                    ),
                ),
                class_name="flex-col items-center w-full",
            ),
            class_name="flex-col items-center p-6 space-y-6 w-full",
        ),
        class_name="flex-col items-center divide-y w-full",
    )


def contract_hospital_pay() -> rx.Component:
    return flex()


def contract_state_pay() -> rx.Component:
    return flex()


def staff_experience_control_slider() -> rx.Component:
    return flex(
        flex(
            rx.text("Experience", class_name="text-xl"),
            class_name="flex-col bg-teal-100 items-center p-2 w-full",
        ),
        flex(
            rx.text(
                f"{HospitalState.selected_experience} year(s)",
                class_name="text-xl font-bold",
            ),
            rx.slider(
                default_value=HospitalState.selected_experience,
                min=0,
                max=26,
                on_change=HospitalState.set_slider,
                class_name="p-4",
            ),
            rx.text("Set slider to view rates by experience", class_name="italic"),
            class_name="flex-col items-center p-6 space-y-2 w-full",
        ),
        class_name="flex-col items-center divide-y w-full",
    )


def staff_employment_type_selection() -> rx.Component:
    return flex(
        flex(
            rx.text("Employment Type", class_name="text-xl"),
            class_name="flex-col bg-teal-100 items-center p-2 w-full",
        ),
        flex(
            rx.radio(
                ["Full-time", "Part-time"],
                direction="row",
                size="3",
                spacing="3",
                value=HospitalState.selected_employment_type,
                on_change=HospitalState.setvar("selected_employment_type"),
            ),
            rx.text("Select to view pay for that employment type", class_name="italic"),
            class_name="flex-col items-center space-y-4 p-6 w-full",
        ),
        class_name="flex-col items-center divide-y w-full",
    )


def units() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("stethoscope", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                rx.heading("Units", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
        class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        flex(
            units_content(),
            class_name="flex-col items-center p-4 space-y-4 w-full",
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )


def units_content() -> rx.Component:
    return rx.cond(
        HospitalState.units_areas_roles_for_units,
        flex(
            unit_area_role_hospital_scores(),
            unit_area_role_rankings(),
            class_name="flex-col items-center space-y-6 divide-y w-full",
        ),
        flex(
            rx.text("Nothing yet, check back later!"),
            class_name="flex-col items-center p-6 w-full",
        ),
    )


def unit_area_role_hospital_scores() -> rx.Component:
    return flex(
        flex(
            flex(
                rx.select(
                    HospitalState.units_areas_roles_for_units,
                    placeholder="Hospital Overall",
                    value=HospitalState.selected_unit,
                    label="Units/Areas/Roles",
                    on_change=HospitalState.set_selected_unit,
                ),
                rx.button(
                    "Clear selection", on_click=HospitalState.set_selected_unit("")
                ),
                class_name="flex-row space-x-2",
            ),
            class_name="flex-col items-center justify-items-center w-full",
        ),
        flex(
            rx.cond(
                HospitalState.selected_unit,
                rx.heading(HospitalState.selected_unit),
                rx.heading("Hospital Overall"),
            ),
            class_name="flex-col items-center p-6 w-full",
        ),
        flex(
            flex(
                rx.text(HospitalState.filtered_unit_info["comp_mean"]),
                rx.text("Compensation"),
                class_name="flex-col items-center w-full",
            ),
            flex(
                rx.text(HospitalState.filtered_unit_info["assign_mean"]),
                rx.text("Assignment"),
                class_name="flex-col items-center w-full",
            ),
            flex(
                rx.text(HospitalState.filtered_unit_info["staffing_mean"]),
                rx.text("Staffing"),
                class_name="flex-col items-center w-full",
            ),
            flex(
                rx.text(HospitalState.filtered_unit_info["overall_mean"]),
                rx.text("Overall"),
                class_name="flex-col items-center w-full",
            ),
            class_name="flex-row items-center justify-between w-full",
        ),
        class_name="flex-col items-center w-full",
    )


def unit_area_role_rankings() -> rx.Component:
    return flex(
        rx.text("Unit ratings placeholder"),
        class_name="flex-col items-center pt-6 w-full",
    )


def reviews() -> rx.Component:
    """Free response section."""
    return flex(
        flex(
            flex(
                flex(
                    rx.icon("speech", class_name="mr-3 h-8 w-8"),
                    rx.heading("Reviews", class_name="font-bold text-2xl"),
                    class_name="flex-row items-center",
                ),
                class_name="flex-col items-center lg:items-start w-full lg:w-3/12",
            ),
            flex(
                review_content(),
                class_name="flex-col items-center rounded shadow-lg bg-white md:justify-self-center space-y-6 md:space-y-10 p-6 lg:p-12 w-full",
            ),
            class_name="flex-col lg:flex-row space-y-6 lg:space-y-0 w-full",
        ),
        class_name="flex-row p-6 lg:p-12 w-full",
    )


def review_content() -> rx.Component:
    return flex(
        rx.cond(
            HospitalState.review_info,
            # REVIEWS PRESENT
            flex(
                rx.cond(
                    HospitalState.units_areas_roles_for_reviews,
                    review_filters(),
                ),
                flex(
                    rx.foreach(
                        HospitalState.filtered_review_info,
                        response_card,
                    ),
                    class_name="flex-col divide-y w-full",
                ),
                class_name="flex-col space-y-3 w-full",
            ),
            # REVIEWS NOT PRESENT
            flex(
                rx.text("Nothing yet, check back later!"),
                class_name="flex-col items-center p-6 w-full",
            ),
        ),
        class_name="flex-col items-center w-full",
    )


def review_filters() -> rx.Component:
    return flex(
        rx.select(
            HospitalState.units_areas_roles_for_reviews,
            value=HospitalState.review_filter_units_areas_roles,
            placeholder="All units/areas/roles",
            label="Select a unit/area/role",
            size="2",
            on_change=HospitalState.set_review_filter_units_areas_roles,
            width=["50%", "50%", "auto", "auto", "auto"],
        ),
        rx.select(
            ["Most Recent", "Most Helpful"],
            value=HospitalState.review_sorted,
            placeholder="Sort by",
            label="Select a sort method",
            size="2",
            on_change=HospitalState.set_review_sorted,
            width=["50%", "50%", "auto", "auto", "auto"],
        ),
        rx.button(
            rx.text("Clear filters"),
            size="2",
            on_click=[
                HospitalState.set_review_filter_units_areas_roles(""),
                HospitalState.set_review_sorted(""),
            ],
            width=["50%", "50%", "auto", "auto", "auto"],
        ),
        class_name="flex-col md:flex-row items-center md:justify-center space-y-2 md:space-y-0 md:space-x-2 w-full",
    )


def response_card(review: dict[str, str]) -> rx.Component:
    """
    Renders the review card for the hospital overview.

    Dict:
        user_id
        created_at
        comp_input_comments
        assign_input_comments
        staffing_input_comments
        unit
        area_role

    """
    return flex(
        rx.vstack(
            rx.hstack(
                rx.cond(
                    review["unit"],
                    rx.text(review["unit"], weight="bold"),
                    rx.text(review["area_role"], weight="bold"),
                ),
                rx.spacer(),
                flex(
                    rx.text(review["formatted_created_at"]),
                ),
                width="100%",
            ),
            rx.cond(
                review["comp_input_comments"],
                flex(rx.text(review["comp_input_comments"]), width="100%"),
            ),
            rx.cond(
                review["assign_input_comments"],
                flex(rx.text(review["assign_input_comments"]), width="100%"),
            ),
            rx.cond(
                review["staffing_input_comments"],
                flex(rx.text(review["staffing_input_comments"]), width="100%"),
            ),
            flex(
                rx.cond(
                    review["user_has_liked"],
                    # If user has liked the review
                    flex(
                        rx.button(
                            rx.icon("thumbs-up", size=18),
                            rx.text(review["likes_number"]),
                            variant="ghost",
                            cursor="pointer",
                            _hover={"bg": "none"},
                            on_click=HospitalState.event_state_like_unlike_review(
                                review
                            ),
                        ),
                        rx.text(
                            " - You upvoted.", class_name="text-sm text-teal-600 pl-1"
                        ),
                        class_name="flex-row items-center",
                    ),
                    # If user hasn't liked review
                    flex(
                        rx.button(
                            rx.icon("thumbs-up", size=18),
                            rx.text(review["likes_number"]),
                            variant="ghost",
                            cursor="pointer",
                            _hover={"bg": "none"},
                            on_click=HospitalState.event_state_like_unlike_review(
                                review
                            ),
                        )
                    ),
                ),
                class_name="flex-row items-center justify-center w-full",
            ),
            class_name="w-full",
        ),
        class_name="py-6 w-full",
    )
