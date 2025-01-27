from ..components import (
    flex,
    footer,
    navbar,
    report_protected,
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
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(
            heading(),
            staff_pay(),
            travel_pay(),
            units_roles(),
            reviews(),
            class_name="flex-col items-center space-y-12 px-4 py-12 w-full max-w-screen-lg",
    )


def heading() -> rx.Component:
    return rx.flex(
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
                text(HospitalState.hospital_info["hosp_addr"], class_name="text-sm"),
                loading=~rx.State.is_hydrated
                ),
            rx.skeleton(
                text(
                    f'{HospitalState.hospital_info["hosp_city"]}, {HospitalState.hospital_info["hosp_state_abbr"]} {HospitalState.hospital_info["hosp_zip"]}',
                    class_name="text-sm"
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
            text("Hospital Average", class_name="text-lg"),
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
                                text(HospitalState.ft_pay_hospital_formatted['hourly'], class_name="text-2xl"),
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
                                text(HospitalState.pt_pay_hospital_formatted['hourly'], class_name="text-2xl"),
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
                                text(HospitalState.ft_pay_hospital_formatted["yearly"], class_name="text-2xl"),
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
                                text(HospitalState.pt_pay_hospital_formatted["yearly"], class_name="text-2xl"),
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
                rx.icon("triangle-alert", class_name="h-3 w-3 stroke-orange-500"),
                rx.text("LIMITED DATA. ESTIMATES MAY BE OFF.", class_name="text-xs text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_hospital_average == "Part-time") &
            (HospitalState.pt_pay_hospital_info_limited) &
            (HospitalState.extrapolated_pt_pay_hospital),
            flex(
                rx.icon("triangle-alert", class_name="h-3 w-3 stroke-orange-500"),
                rx.text("LIMITED DATA. ESTIMATES MAY BE OFF.", class_name="text-xs text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_hospital_average == "Full-time") & (~HospitalState.extrapolated_ft_pay_hospital),
            rx.flex(
                rx.icon("ban", class_name="h-3 w-3 stroke-rose-500"),
                rx.text("NO PAY DATA AVAILABLE YET.", class_name="text-xs text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_hospital_average == "Part-time") & (~HospitalState.extrapolated_pt_pay_hospital),
            flex(
                rx.icon("ban", class_name="h-3 w-3 stroke-rose-500"),
                rx.text("NO PAY DATA AVAILABLE YET.", class_name="text-xs text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        class_name="flex-col items-center divide-y dark:divide-zinc-500 w-full"
    )


def state_average() -> rx.Component:
    return flex(
        flex(
            text(f"{HospitalState.hospital_info['hosp_state']} Average", class_name="text-lg"),
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
                                text(HospitalState.ft_pay_state_formatted['hourly'], class_name="text-2xl"),
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
                                text(HospitalState.pt_pay_state_formatted['hourly'], class_name="text-2xl"),
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
                                text(HospitalState.ft_pay_state_formatted["yearly"], class_name="text-2xl"),
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
                                text(HospitalState.pt_pay_state_formatted["yearly"], class_name="text-2xl"),
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
                rx.text("LIMITED DATA. ESTIMATES MAY BE OFF.", class_name="text-xs text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_state_average == "Full-time") &
            (HospitalState.ft_pay_state_info_limited) &
            (HospitalState.extrapolated_ft_pay_state),
            flex(
                rx.icon("triangle-alert", class_name="h-3 w-3 stroke-orange-500"),
                rx.text("LIMITED DATA. ESTIMATES MAY OFF.", class_name="text-xs text-orange-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_state_average == "Full-time") & (~HospitalState.extrapolated_ft_pay_state),
            flex(
                rx.icon("ban", class_name="h-3 w-3 stroke-rose-500"),
                rx.text("NO PAY DATA AVAILABLE YET.", class_name="text-xs text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        rx.cond(
            (HospitalState.selected_state_average == "Part-time") & (~HospitalState.extrapolated_pt_pay_state),
            flex(
                rx.icon("ban", class_name="h-3 w-3 stroke-rose-500"),
                rx.text("NO PAY DATA AVAILABLE YET.", class_name="text-xs text-rose-500"),
                class_name="flex-row items-center justify-center p-1 space-x-2 w-full"
            )
        ),
        class_name="flex-col items-center divide-y w-full"
    )

def experience_slider() -> rx.Component:
    return flex(
        flex(
            text("Experience -", class_name="text-lg text-nowrap"),
            flex(
                rx.cond(
                    HospitalState.selected_experience <= 25,
                    rx.skeleton(
                        text(
                            f"{HospitalState.selected_experience} year(s)",
                            class_name="text-lg text-nowrap pl-1"
                        ),
                        loading=~rx.State.is_hydrated
                    ),
                    rx.skeleton(
                        text(
                            "More than 25 years",
                            class_name="text-lg text-nowrap pl-1"
                        ),
                        loading=~rx.State.is_hydrated
                    )
                )
            ),
            class_name="flex-col md:flex-row items-center px-6 py-2 w-full"
        ),
        flex(
            text("0 YEARS", class_name="text-xs pr-4 text-nowrap"),
            rx.slider(
                default_value=HospitalState.selected_experience,
                min=0,
                max=26,
                color_scheme="teal",
                on_change=HospitalState.set_slider,
                class_name="w-full",
            ),
            text("> 25 YEARS", class_name="text-xs pl-4 text-nowrap"),
            class_name="flex-row items-center p-5 w-full"
        ),
        class_name="flex-col items-center divide-y w-full"
    )



def travel_pay() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("plane", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Travel Pay", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
            class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        flex(
            text("No reports yet, check back later!"),
            class_name="flex-col items-center p-6 w-full",
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )


def units_roles() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("stethoscope", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Units/Roles", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
        class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),

        # Units subheader and unit selector.
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            flex(
                rx.cond(
                    HospitalState.selected_unit,
                    text(HospitalState.selected_unit, class_name="text-lg font-bold"),
                    text("Hospital Overall", class_name="text-lg")
                ),
                rx.spacer(),
                flex(
                    rx.select(
                        HospitalState.units_areas_roles_for_units,
                        placeholder="Hospital Overall",
                        value=HospitalState.selected_unit,
                        label="Units/Areas/Roles",
                        color_scheme="teal",
                        on_change=HospitalState.set_selected_unit,
                    ),
                    solid_button(
                        "Reset", on_click=HospitalState.set_selected_unit("")
                    ),
                    class_name="flex-row space-x-2",
                ),
                class_name="flex-col md:flex-row items-center px-6 py-2 space-y-1 md:space-y-0 w-full"
            ),
        ),

        # Units grades.
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            # If there are units to select.
            flex(
                flex(
                    rx.text(HospitalState.filtered_unit_info["comp_mean"], class_name="text-2xl"),
                    rx.spacer(),
                    rx.text("COMPENSATION", class_name="text-sm"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                flex(
                    rx.text(HospitalState.filtered_unit_info["assign_mean"], class_name="text-2xl"),
                    rx.spacer(),
                    rx.text("ASSIGNMENT", class_name="text-sm"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                flex(
                    rx.text(HospitalState.filtered_unit_info["staffing_mean"], class_name="text-2xl"),
                    rx.spacer(),
                    rx.text("STAFFING", class_name="text-sm"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                flex(
                    rx.text(HospitalState.filtered_unit_info["overall_mean"], class_name="text-2xl font-bold"),
                    rx.spacer(),
                    rx.text("OVERALL", class_name="text-sm font-bold"),
                    class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-2 md:space-y-1 w-full",
                ),
                class_name="flex-col md:flex-row items-center justify-between divide-y md:divide-y-0 md:divide-x w-full",
            ),
            flex(
                rx.text("No reports yet, check back later!"),
                class_name="flex-col items-center p-6 w-full",
            ),
        ),

        # Unit rank subheader and filters.
        rx.cond(
            HospitalState.units_areas_roles_for_rankings,
            flex(
                text("Rankings", class_name="text-lg"),
                class_name="flex-col md:flex-row items-center px-6 py-2 space-y-1 md:space-y-0 w-full"
            ),
        ),

        # Unit/Role rankings section.
        rx.cond(
            HospitalState.units_areas_roles_for_rankings,
            flex(
                flex(
                    rx.flex(
                        rx.flex(
                            rx.icon("trophy", class_name="h-4 w-4 stroke-1"),
                            class_name="flex-row items-center justify-center p-2 w-[20%]"
                        ),
                        rx.text("Unit/Role", class_name="text-xs text-center truncate uppercase p-2 w-[80%]"),
                        class_name="divide-x dark:divide-zinc-500 w-[40%]"
                    ),
                    rx.text("Compensation", class_name="text-xs text-center truncate uppercase p-2 w-[15%]"),
                    rx.text("Assignment", class_name="text-xs text-center truncate uppercase p-2 w-[15%]"),
                    rx.text("Staffing", class_name="text-xs text-center truncate uppercase p-2 w-[15%]"),
                    rx.text("Overall", class_name="text-xs text-center truncate uppercase p-2 w-[15%]"),
                    class_name="flex-row items-center divide-x dark:divide-zinc-500 w-full"
                ),
                ranked_items(),
                class_name="flex-col divide-y dark:divide-zinc-500 w-full"
            ),
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )

def ranked_items() -> rx.Component:
    return rx.foreach(HospitalState.units_areas_roles_for_rankings, rank_item)

def rank_item(unit_area_role:dict) -> rx.Component:
    return rx.cond(
        HospitalState.selected_unit == unit_area_role["units_areas_roles"],
        rx.flex(
            rx.flex(
                rx.text(unit_area_role["ranking"], class_name="text-sm font-bold text-center p-2 w-[20%]"),
                rx.text(unit_area_role["units_areas_roles"], class_name="text-sm font-bold text-center truncate p-2 w-[80%]"),
                class_name="divide-x dark:divide-zinc-500 w-[40%]"
            ),
            rx.text(unit_area_role["comp_mean"], class_name="text-sm font-bold text-center truncate p-2 w-[15%]"),
            rx.text(unit_area_role["assign_mean"], class_name="text-sm font-bold text-center truncate p-2 w-[15%]"),
            rx.text(unit_area_role["staffing_mean"], class_name="text-sm font-bold text-center truncate p-2 w-[15%]"),
            rx.text(unit_area_role["overall_mean"], class_name="text-sm font-bold text-center truncate p-2 w-[15%]"),
            class_name="flex-row bg-zinc-100 dark:bg-zinc-700 items-center divide-x dark:divide-zinc-500 w-full"
        ),
        rx.flex(
            rx.flex(
                rx.text(unit_area_role["ranking"], class_name="text-sm text-center p-2 w-[20%]"),
                rx.text(unit_area_role["units_areas_roles"], class_name="text-sm text-center truncate p-2 w-[80%]"),
                class_name="divide-x dark:divide-zinc-500 w-[40%]"
            ),
            rx.text(unit_area_role["comp_mean"], class_name="text-sm text-center truncate p-2 w-[15%]"),
            rx.text(unit_area_role["assign_mean"], class_name="text-sm text-center truncate p-2 w-[15%]"),
            rx.text(unit_area_role["staffing_mean"], class_name="text-sm text-center truncate p-2 w-[15%]"),
            rx.text(unit_area_role["overall_mean"], class_name="text-sm text-center truncate p-2 w-[15%]"),
            class_name="flex-row items-center divide-x dark:divide-zinc-500 w-full"
        )
    )

def reviews() -> rx.Component:
    """Free response section."""
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("speech", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Reviews", class_name="font-bold text-2xl"),
                class_name="flex-row items-center space-x-2",
            ),
            class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        rx.cond(
            HospitalState.review_info,
            review_filters()
        ),
        rx.cond(
            HospitalState.review_info,
            # REVIEWS PRESENT
            flex(
                rx.foreach(
                    HospitalState.filtered_review_info,
                    response_card,
                ),
                class_name="flex-col divide-y w-full",
            ),
            # REVIEWS NOT PRESENT
            flex(
                rx.text("No reports yet, check back later!"),
                class_name="flex-col items-center p-6 w-full",
            ),
        ),
        class_name="flex-col items-center border rounded divide-y dark:divide-zinc-500 w-full"
    )


def review_filters() -> rx.Component:
    return flex(
        rx.select(
            HospitalState.units_areas_roles_for_reviews,
            value=HospitalState.review_filter_units_areas_roles,
            placeholder="All units/areas/roles",
            label="Select a unit/area/role",
            size="2",
            color_scheme="teal",
            on_change=HospitalState.set_review_filter_units_areas_roles,
            width=["100%", "100%", "auto", "auto", "auto"]
        ),
        rx.select(
            ["Most Recent", "Most Helpful"],
            value=HospitalState.review_sorted,
            placeholder="Sort by",
            label="Select a sort method",
            size="2",
            color_scheme="teal",
            on_change=HospitalState.set_review_sorted,
            width=["100%", "100%", "auto", "auto", "auto"]
        ),
        solid_button(
            rx.text("Clear filters"),
            size="2",
            on_click=[
                HospitalState.set_review_filter_units_areas_roles(""),
                HospitalState.set_review_sorted(""),
            ],
            width=["100%", "100%", "auto", "auto", "auto"]
        ),
        class_name="flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 items-center justify-center p-2 w-full"
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
            flex(
                rx.cond(
                    review["unit"],
                    rx.text(review["unit"], class_name="text-lg"),
                    rx.text(review["area_role"], class_name="text-lg"),
                ),
                rx.spacer(),
                flex(
                    text(review["formatted_created_at"], class_name="text-xs uppercase"),
                ),
                class_name="flex-row items-center w-full"
            ),
            rx.cond(
                review["comp_input_comments"],
                flex(text(review["comp_input_comments"]), width="100%"),
            ),
            rx.cond(
                review["assign_input_comments"],
                flex(text(review["assign_input_comments"]), width="100%"),
            ),
            rx.cond(
                review["staffing_input_comments"],
                flex(text(review["staffing_input_comments"]), width="100%"),
            ),
            flex(
                rx.cond(
                    review["user_has_liked"],
                    # If user has liked the review
                    flex(
                        rx.button(
                            rx.icon("heart", class_name="h-5 w-5 pr-1 stroke-rose-500 fill-rose-500"),
                            rx.text(review["likes_number"], class_name="text-rose-500"),
                            variant="ghost",
                            cursor="pointer",
                            _hover={"bg": "none"},
                            on_click=HospitalState.event_state_like_unlike_review(
                                review
                            ),
                        ),
                        class_name="flex-row items-center",
                    ),
                    # If user hasn't liked review
                    flex(
                        rx.button(
                            rx.icon("heart", class_name="h-5 w-5 pr-1 stroke-rose-500"),
                            rx.text(review["likes_number"], class_name="text-rose-500"),
                            variant="ghost",
                            cursor="pointer",
                            _hover={"bg": "none"},
                            on_click=HospitalState.event_state_like_unlike_review(
                                review
                            ),
                        )
                    ),
                ),
                class_name="flex-row items-center justify-end w-full",
            ),
            class_name="w-full",
        ),
        class_name="p-4 w-full",
    )