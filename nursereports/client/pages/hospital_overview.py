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
        BaseState.event_state_requires_report,
        HospitalState.event_state_load_hospital_info,
    ],
)
@report_protected
def hospital_overview() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center dark:bg-zinc-900 min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(
            heading(),
            staff_pay(),
            travel_pay(),
            reviews(),
            class_name="flex-col items-center space-y-4 md:space-y-12 px-4 py-4 md:py-20 w-full max-w-screen-md",
    )


def heading() -> rx.Component:
    return flex(
        # rx.flex(
        #     rx.flex(
        #         rx.icon("hospital", class_name="h-6 w-6 stroke-zinc-700 dark:stroke-teal-800"),
        #         text("Hospital Overview", class_name="text-2xl font-bold"),
        #         class_name="flex-row items-center space-x-2"
        #     ),
        #     class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-4 w-full"
        # ),

        # Hospital information section.
        rx.flex(
            rx.flex(
                rx.skeleton(
                    text(HospitalState.hospital_info["hosp_name"], class_name="font-bold text-center text-3xl"),
                    loading=~rx.State.is_hydrated
                ),
                rx.skeleton(
                    text(HospitalState.hospital_info["hosp_addr"], class_name="text-xl"),
                    loading=~rx.State.is_hydrated
                    ),
                rx.skeleton(
                    text(
                        f'{HospitalState.hospital_info["hosp_city"]}, {HospitalState.hospital_info["hosp_state_abbr"]} {HospitalState.hospital_info["hosp_zip"]}',
                        class_name="text-xl"
                    ),
                    loading=~rx.State.is_hydrated
                ),
                class_name="flex-col items-center space-y-1 w-full",
            ),
            class_name="p-8 w-full"
        ),

        # Hospital buttons.
        rx.flex(
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
        ),
        class_name="flex-col items-center border rounded shadow-lg divide-y dark:divide-zinc-700 w-full"
    )


def staff_pay() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("banknote", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Staff Pay", class_name="text-xl font-bold"),
                class_name="flex-row items-center space-x-2",
            ),
            class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        hospital_average(),
        # state_average(),
        experience_slider(),
        class_name="flex-col items-center border rounded shadow-lg divide-y dark:divide-zinc-700 w-full"
    )

def hospital_average() -> rx.Component:
    return flex(
        flex(
            rx.flex(
                text("Hospital Average", class_name="text-xl"),
                class_name="flex justify-center md:justify-start w-full"
            ),
            rx.segmented_control.root(
                rx.segmented_control.item("Full-time", value="Full-time"),
                rx.segmented_control.item("Part-time", value="Part-time"),
                on_change=HospitalState.setvar("selected_hospital_average"),
                value=HospitalState.selected_hospital_average
            ),
            class_name="flex-col md:flex-row items-center p-4 space-y-4 md:space-y-0 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
                    ),
                )
            ),
            class_name="flex-row divide-x dark:divide-zinc-700 w-full"
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
        class_name="flex-col items-center divide-y dark:divide-zinc-700 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("HOURLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
                                rx.icon("ban", class_name="h-7 w-7 stroke-zinc-200 m-1"),
                                loading=~rx.State.is_hydrated
                            )
                        ),
                        text("YEARLY", class_name="text-xs"),
                        class_name="flex-col items-center p-4 w-full"
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
        class_name="flex-col items-center divide-y dark:divide-zinc-700 w-full"
    )

def experience_slider() -> rx.Component:
    return flex(
        flex(
            text("Experience -", class_name="text-xl text-nowrap"),
            flex(
                rx.cond(
                    HospitalState.selected_experience <= 25,
                    rx.skeleton(
                        text(
                            f"{HospitalState.selected_experience} year(s)",
                            class_name="text-xl text-nowrap pl-1"
                        ),
                        loading=~rx.State.is_hydrated
                    ),
                    rx.skeleton(
                        text(
                            "More than 25 years",
                            class_name="text-xl text-nowrap pl-1"
                        ),
                        loading=~rx.State.is_hydrated
                    )
                )
            ),
            class_name="flex-col md:flex-row items-center p-4 w-full"
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
        class_name="flex-col items-center divide-y dark:divide-zinc-700 w-full"
    )

def travel_pay() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("plane", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                text("Travel Pay", class_name="text-xl font-bold"),
                class_name="flex-row items-center space-x-2",
            ),
            class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),
        flex(
            text("No reports yet, check back later!"),
            class_name="flex-col items-center p-6 w-full",
        ),
        class_name="flex-col items-center border rounded shadow-lg divide-y dark:divide-zinc-700 w-full"
    )


def reviews() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.icon("message-circle", class_name="stroke-zinc-700 dark:stroke-teal-800 h-6 w-6"),
                rx.flex(
                    text("Reviews", class_name="text-xl font-bold"),
                    text("-", class_name="text-xl font-bold"),
                    text(HospitalState.selected_unit, class_name="font-bold text-xl"),
                    class_name="space-x-2"
                ),
                class_name="flex-row items-center space-x-2",
            ),
        class_name="flex-col items-start bg-zinc-100 dark:bg-zinc-800 p-2 w-full"
        ),

        # Units subheader and unit selector.
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            flex(
                flex(
                    rx.flex(
                        text("Select: "),
                        class_name="flex justify-center items-center whitespace-nowrap w-auto"
                    ),
                    rx.flex(
                        rx.select(
                            HospitalState.units_areas_roles_for_units,
                            placeholder="Hospital Overall",
                            value=HospitalState.selected_unit,
                            position="popper",
                            color_scheme="teal",
                            on_change=HospitalState.set_selected_unit,
                            width="100%"
                        ),
                        class_name="w-full"
                    ),
                    class_name="flex-row space-x-4 w-full",
                ),
                class_name="flex-col md:flex-row items-center p-4 space-y-4 md:space-y-0 w-full"
            ),
        ),

        # REVIEWS RATING
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            # If there are units to select.
            flex(
                # COMPENSATION POPOVER / RATING
                rx.popover.root(
                    rx.popover.trigger(
                        flex(
                            convert_to_large_emoji(HospitalState.selected_unit_info["comp_overall"]),
                            rx.spacer(),
                            rx.flex(
                                rx.text("COMPENSATION", class_name="text-sm select-none"),
                                rx.icon("circle-help", class_name="stroke-zinc-700 dark:stroke-zinc-700"),
                                class_name="md:flex-col space-x-2 md:space-x-0 space-y-0 md:space-y-2 items-center"
                            ),
                            class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-4 md:space-y-1 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                        ),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text("Compensation is a subjective nurse-rated score."),
                            rx.text("This score suggests how satisfied nurses are with their overall pay and benefits package."),
                            class_name="space-y-2 flex-col max-w-sm"
                        ),
                        align="center",
                        class_name="dark:bg-zinc-800"
                    )
                ),

                # ASSIGNMENT POPOVER / RATING
                rx.popover.root(
                    rx.popover.trigger(
                        flex(
                            convert_to_large_emoji(HospitalState.selected_unit_info["assign_overall"]),
                            rx.spacer(),
                            rx.flex(
                                rx.text("ASSIGNMENT", class_name="text-sm select-none"),
                                rx.icon("circle-help", class_name="stroke-zinc-700 dark:stroke-zinc-700"),
                                class_name="md:flex-col space-x-2 md:space-x-0 space-y-0 md:space-y-2 items-center"
                            ),
                            class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-4 md:space-y-1 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                        ),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text("Assignment is a subjective nurse-rated score."),
                            rx.text("This score strongly tracks workplace culture and day-to-day experience alongside aides, co-workers, management, physicians, etc."),
                            class_name="space-y-2 flex-col max-w-sm"
                        ),
                        align="center",
                        class_name="dark:bg-zinc-800"
                    )
                ),

                # STAFFING POPVER / RATING
                rx.popover.root(
                    rx.popover.trigger(
                        flex(
                            convert_to_large_emoji(HospitalState.selected_unit_info["staff_overall"]),
                            rx.spacer(),
                            rx.flex(
                                rx.text("STAFFING", class_name="text-sm select-none"),
                                rx.icon("circle-help", class_name="stroke-zinc-700 dark:stroke-zinc-700"),
                                class_name="md:flex-col space-x-2 md:space-x-0 space-y-0 md:space-y-2 items-center"
                            ),
                            class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-4 md:space-y-1 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                        ),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text("Staffing is a subjective nurse-rated score."),
                            rx.text("This is an indicator of how fair ratios and daily workloads might feel as a result of staffing decisions."),
                            class_name="space-y-2 flex-col max-w-sm"
                        ),
                        align="center",
                        class_name="dark:bg-zinc-800"
                    )
                ),

                # OVERALL POPOVER / RATING
                rx.popover.root(
                    rx.popover.trigger(
                        flex(
                            convert_to_large_emoji(HospitalState.selected_unit_info["overall"]),
                            rx.spacer(),
                            rx.flex(
                                rx.text("OVERALL", class_name="text-sm font-bold select-none"),
                                rx.icon("circle-help", class_name="stroke-zinc-700 dark:stroke-zinc-700"),
                                class_name="md:flex-col space-x-2 md:space-x-0 space-y-0 md:space-y-2 items-center"
                            ),
                            class_name="flex-row-reverse md:flex-col items-center justify-center px-6 py-4 md:space-y-1 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                        ),
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text("This is an average using compensation, assignment, and staffing scores."),
                            rx.text("This suggests the general satisfaction with the workplace across the major categories."),
                            class_name="space-y-2 flex-col max-w-sm"
                        ),
                        align="center",
                        class_name="dark:bg-zinc-800"
                    )
                ),
                class_name="flex-col md:flex-row items-center justify-between divide-y md:divide-y-0 md:divide-x dark:divide-zinc-700 w-full",
            ),
            flex(
                rx.text("No reports yet, check back later!"),
                class_name="flex-col items-center p-6 w-full",
            ),
        ),
        comments(),
        class_name="flex-col items-center border rounded shadow-lg divide-y dark:divide-zinc-700 w-full"
    )

def convert_to_large_emoji(rating: str) -> rx.Component:
    return rx.match(
        rating,
        (1, rx.icon("angry", class_name="h-10 w-10 fill-red-400 stroke-[1.5] dark:stroke-zinc-700")),
        (2, rx.icon("frown", class_name="h-10 w-10 fill-orange-400 stroke-[1.5] dark:stroke-zinc-700")),
        (3, rx.icon("meh", class_name="h-10 w-10 fill-yellow-200 stroke-[1.5] dark:stroke-zinc-700")),
        (4, rx.icon("smile", class_name="h-10 w-10 fill-green-500 stroke-[1.5] dark:stroke-zinc-700")),
        (5, rx.icon("laugh", class_name="h-10 w-10 fill-blue-300 stroke-[1.5] dark:stroke-zinc-700")),
    )

def comments() -> rx.Component: 
    """Comments section."""
    return rx.flex(
        rx.cond(
            HospitalState.review_info,
            # REVIEWS PRESENT
            flex(
                rx.foreach(
                    HospitalState.paginated_review_info,
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

        # Paginated reviews if multiple pages.
        rx.cond(
            (HospitalState.num_review_pages > 1),
            rx.flex(
                rx.flex(
                    rx.icon("arrow-left"),
                    on_click=HospitalState.previous_review_page,
                    class_name="flex justify-center p-4 w-full active:bg-zinc-200 transition-colors duration-75 cursor-pointer"
                ),
                rx.text(
                    f"{HospitalState.current_review_page} of {HospitalState.num_review_pages}",
                    class_name="flex justify-center p-4 w-full"
                ),
                rx.flex(
                    rx.icon("arrow-right"),
                    on_click=HospitalState.next_review_page,
                    class_name="flex justify-center p-4 w-full active:bg-zinc-200 transition-colors duration-75 cursor-pointer"
                ),
                class_name="flex-row divide-x dark:divide-zinc-700 w-full"
            ),
        ),
        class_name="flex-col items-center divide-y dark:divide-zinc-700 w-full"
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
        rx.flex(
            flex(
                rx.text(review["units_areas_roles"], class_name="text-lg"),
                rx.spacer(),
                flex(
                    text(review["time_ago"], class_name="text-xs uppercase"),
                ),
                class_name="flex-row items-center w-full"
            ),
            rx.flex(
                rx.cond(
                    review["comp_comments"],
                    flex(text(review["comp_comments"]), width="100%"),
                ),
                rx.cond(
                    review["assign_comments"],
                    flex(text(review["assign_comments"]), width="100%"),
                ),
                rx.cond(
                    review["staff_comments"],
                    flex(text(review["staffing_comments"]), width="100%"),
                ),
                class_name="flex-col space-y-1 p-4 w-full"
            ),
            # flex(
            #     rx.cond(
            #         review["user_has_liked"],
            #         # If user has liked the review
            #         flex(
            #             rx.button(
            #                 rx.icon("heart", class_name="h-5 w-5 pr-1 stroke-rose-500 fill-rose-500"),
            #                 rx.text(review["likes_number"], class_name="text-rose-500"),
            #                 variant="ghost",
            #                 cursor="pointer",
            #                 _hover={"bg": "none"},
            #                 on_click=HospitalState.event_state_like_unlike_review(
            #                     review
            #                 ),
            #             ),
            #             class_name="flex-row items-center",
            #         ),
            #         # If user hasn't liked review
            #         flex(
            #             rx.button(
            #                 rx.icon("heart", class_name="h-5 w-5 pr-1 stroke-rose-500"),
            #                 rx.text(review["likes_number"], class_name="text-rose-500"),
            #                 variant="ghost",
            #                 cursor="pointer",
            #                 _hover={"bg": "none"},
            #                 on_click=HospitalState.event_state_like_unlike_review(
            #                     review
            #                 ),
            #             )
            #         ),
            #     ),
            #     class_name="flex-row items-center justify-end w-full",
            # ),
            class_name="flex-col w-full",
        ),
        class_name="p-4 w-full",
    )