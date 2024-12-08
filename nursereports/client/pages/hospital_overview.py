from ..components import (
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
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-teal-300",
    )


def content() -> rx.Component:
    return flex(
            heading(),
            staff_pay(),
            travel_pay(),
            units(),
            reviews(),
            class_name="flex-col items-center space-y-12 px-4 py-8 w-full max-w-screen-md",
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
                text(HospitalState.hospital_info["hosp_name"], class_name="font-bold text-center text-2xl"),
                loading=~rx.State.is_hydrated
            ),
            rx.skeleton(
                text(HospitalState.hospital_info["hosp_addr"], class_name="italic text-sm"),
                loading=~rx.State.is_hydrated
                ),
            rx.skeleton(
                text(
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


def staff_pay() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("banknote", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Staff Pay", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
        class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        hospital_average(),
        state_average(),
        experience_slider(),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )

def hospital_average() -> rx.Component:
    return flex(
        flex(
            text("Hospital Average", class_name="text-xl font-bold"),
            rx.spacer(),
            rx.segmented_control.root(
                rx.segmented_control.item("Full-time", value="Full-time"),
                rx.segmented_control.item("Part-time", value="Part-time"),
                on_change=HospitalState.setvar("selected_hospital_average"),
                value=HospitalState.selected_hospital_average
            ),
            class_name="flex-col md:flex-row items-center px-6 py-2 space-y-1 md:space-y-0 w-full"
        ),
        flex(
            # Displays hourly pay.
            rx.match(
                HospitalState.selected_hospital_average,
               ("Full-time",
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_ft_pay_hospital,
                            rx.skeleton(
                                text(HospitalState.ft_pay_hospital_formatted['hourly'], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    )
               ),
               ("Part-time", 
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_pt_pay_hospital,
                            rx.skeleton(
                                text(HospitalState.pt_pay_hospital_formatted['hourly'], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    )
                ),
            ),
            # Displays yearly pay.
            rx.match(
                HospitalState.selected_hospital_average,
               ("Full-time",
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_ft_pay_hospital,
                            rx.skeleton(
                                text(HospitalState.ft_pay_hospital_formatted["yearly"], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    ),
                ),
               ("Part-time",
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_pt_pay_hospital,
                            rx.skeleton(
                                text(HospitalState.pt_pay_hospital_formatted["yearly"], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    ),
                )
            ),
            class_name="flex-row divide-x w-full"
        ),

        # Callouts
        rx.cond(
            (HospitalState.selected_hospital_average == "Full-time") &
            (HospitalState.ft_pay_hospital_info_limited) &
            (HospitalState.extrapolated_ft_pay_hospital),
            flex(
                rx.icon("triangle-alert", class_name="h-4 w-4 stroke-orange-500"),
                rx.text("Data limited. Values may be inaccurate.", class_name="text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_hospital_average == "Part-time") &
            (HospitalState.pt_pay_hospital_info_limited) &
            (HospitalState.extrapolated_pt_pay_hospital),
            flex(
                rx.icon("triangle-alert", class_name="h-4 w-4 stroke-orange-500"),
                rx.text("Data limited. Values may be inaccurate.", class_name="text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_hospital_average == "Full-time") & (~HospitalState.extrapolated_ft_pay_hospital),
            rx.flex(
                rx.icon("ban", class_name="h-4 w-4 stroke-rose-500"),
                rx.text("No pay data available yet.", class_name="text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_hospital_average == "Part-time") & (~HospitalState.extrapolated_pt_pay_hospital),
            flex(
                rx.icon("ban", class_name="h-4 w-4 stroke-rose-500"),
                rx.text("No pay data available yet.", class_name="text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        class_name="flex-col items-center divide-y w-full"
    )


def state_average() -> rx.Component:
    return flex(
        flex(
            text("State Average", class_name="text-xl font-bold"),
            rx.spacer(),
            rx.segmented_control.root(
                rx.segmented_control.item("Full-time", value="Full-time"),
                rx.segmented_control.item("Part-time", value="Part-time"),
                on_change=HospitalState.setvar("selected_state_average"),
                value=HospitalState.selected_state_average
            ),
            class_name="flex-col md:flex-row items-center px-6 py-2 space-y-1 md:space-y-0 w-full"
        ),
        flex(
            # Displays hourly pay.
            rx.match(
                HospitalState.selected_state_average,
               ("Full-time",
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_ft_pay_state,
                            rx.skeleton(
                                text(HospitalState.ft_pay_state_formatted['hourly'], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    )
               ),
               ("Part-time", 
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_pt_pay_state,
                            rx.skeleton(
                                text(HospitalState.pt_pay_state_formatted['hourly'], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    )
                ),
            ),
            # Displays yearly pay.
            rx.match(
                HospitalState.selected_state_average,
               ("Full-time",
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_ft_pay_state,
                            rx.skeleton(
                                text(HospitalState.ft_pay_state_formatted["yearly"], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    ),
                ),
               ("Part-time",
                    flex(
                        rx.cond(
                            HospitalState.extrapolated_pt_pay_state,
                            rx.skeleton(
                                text(HospitalState.pt_pay_state_formatted["yearly"], class_name="text-xl"),
                                loading=~rx.State.is_hydrated
                            ),
                            rx.skeleton(
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-2 w-full"
                    ),
                ),
            ),
            class_name="flex-row divide-x w-full"
        ),
        # Callouts
        rx.cond(
            (HospitalState.selected_state_average == "Full-time") &
            (HospitalState.ft_pay_state_info_limited) &
            (HospitalState.extrapolated_ft_pay_state),
            flex(
                rx.icon("triangle-alert", class_name="h-4 w-4 stroke-orange-500"),
                rx.text("Data limited. Values may be inaccurate.", class_name="text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_state_average == "Full-time") &
            (HospitalState.ft_pay_state_info_limited) &
            (HospitalState.extrapolated_ft_pay_state),
            flex(
                rx.icon("triangle-alert", class_name="h-4 w-4 stroke-orange-500"),
                rx.text("Data limited. Values may be inaccurate.", class_name="text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_state_average == "Full-time") & (~HospitalState.extrapolated_ft_pay_state),
            flex(
                rx.icon("ban", class_name="h-4 w-4 stroke-rose-500"),
                rx.text("No pay data available yet.", class_name="text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_state_average == "Part-time") & (~HospitalState.extrapolated_pt_pay_state),
            flex(
                rx.icon("ban", class_name="h-4 w-4 stroke-rose-500"),
                rx.text("No pay data available yet.", class_name="text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        class_name="flex-col items-center divide-y w-full"
    )

def experience_slider() -> rx.Component:
    return flex(
        flex(
            text("Experience", class_name="text-xl font-bold"),
            class_name="flex-col md:flex-row items-center px-6 py-2 w-full"
        ),
        flex(
            rx.cond(
                HospitalState.selected_experience <= 25,
                text(
                    f"{HospitalState.selected_experience} year(s)",
                    class_name="text-lg text-nowrap p-2"
                ),
                text(
                    "More than 25 years",
                    class_name="text-lg text-nowrap p-2"
                )
            ),
            class_name="flex-col items-center w-full"
        ),
        flex(
            text("New Grad", class_name="pr-4 text-nowrap"),
            rx.slider(
                default_value=HospitalState.selected_experience,
                min=0,
                max=26,
                color_scheme="teal",
                on_change=HospitalState.set_slider,
                class_name="w-full",
            ),
            text("> 25 years", class_name="pl-4 text-nowrap"),
            class_name="flex-row items-center p-5 w-full"
        ),
        class_name="flex-col items-center divide-y w-full"
    )



def travel_pay() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("banknote", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Travel Pay", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
        class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        flex(
            text("PLACEHOLDER", class_name="text-xs"),
            class_name="flex-col items-center p-4 w-full",
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
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

        # Units subheader and unit selector.
        flex(
            rx.cond(
                HospitalState.selected_unit,
                text(HospitalState.selected_unit, class_name="text-xl font-bold"),
                text("Hospital Overall", class_name="text-xl font-bold")
            ),
            rx.spacer(),
            flex(
                rx.select(
                    HospitalState.units_areas_roles_for_units,
                    placeholder="Hospital Overall",
                    value=HospitalState.selected_unit,
                    label="Units/Areas/Roles",
                    on_change=HospitalState.set_selected_unit,
                ),
                solid_button(
                    "Reset", on_click=HospitalState.set_selected_unit("")
                ),
                class_name="flex-row space-x-2",
            ),
            class_name="flex-col md:flex-row items-center px-6 py-2 space-y-1 md:space-y-0 w-full"
        ),

        # Units grades.
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            # If there are units to select.
            flex(
                flex(
                    rx.text(HospitalState.filtered_unit_info["comp_mean"], class_name="text-4xl"),
                    rx.spacer(),
                    rx.text("Compensation"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                flex(
                    rx.text(HospitalState.filtered_unit_info["assign_mean"], class_name="text-4xl"),
                    rx.spacer(),
                    rx.text("Assignment"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                flex(
                    rx.text(HospitalState.filtered_unit_info["staffing_mean"], class_name="text-4xl"),
                    rx.spacer(),
                    rx.text("Staffing"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                flex(
                    rx.text(HospitalState.filtered_unit_info["overall_mean"], class_name="text-4xl font-bold"),
                    rx.spacer(),
                    rx.text("Overall", class_name="font-bold"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                class_name="flex-col md:flex-row items-center justify-between divide-y md:divide-y-0 md:divide-x w-full",
            ),
            flex(
                rx.text("Nothing yet, check back later!"),
                class_name="flex-col items-center p-6 w-full",
            ),
        ),
        class_name="flex-col items-center border rounded divide-y w-full"
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
