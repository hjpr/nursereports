from ..components import (
    flex,
    footer,
    login_protected,
    navbar,
    outline_button,
    text
)

from ...states import (
    BaseState,
    ReportState,
    constants_types
)

import reflex as rx


@rx.page(
    route="/report/[report_mode]/staffing",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def staffing_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center w-full"
    )


def content() -> rx.Component:
    return rx.flex(
        staffing(),
        class_name="flex-col items-center space-y-12 px-4 py-14 md:py-20 w-full max-w-screen-sm"
    )


def staffing() -> rx.Component:
    return rx.flex(
        rx.flex(
            text("Staffing", class_name="text-2xl font-bold"),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-6 w-full",
        ),
        flex(

            # Does your assignment generally have set patient ratios?
            rx.flex(
                    rx.flex(
                        rx.text("Does your assignment have patient ratios?"),
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_select_ratio,
                                rx.icon("circle-check-big", class_name="stroke-green-400"),
                                rx.icon("circle-alert", class_name="stroke-zinc-200"),
                            ),
                            class_name="pl-4"
                        ),
                        class_name="flex-row justify-between w-full"
                    ),
                rx.select(
                    constants_types.STAFFING_SELECT_RATIO_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.staffing_select_ratio,
                    position="popper",
                    on_change=ReportState.set_staffing_select_ratio,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col p-4 space-y-2 w-full",
            ),

            # What is your average nurse : patient ratio?
            rx.cond(
                ReportState.staffing_select_ratio == "Yes",
                rx.flex(
                    rx.flex(
                        rx.text("What is your average nurse : patient ratio?"),
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_input_actual_ratio,
                                rx.icon("circle-check-big", class_name="stroke-green-400"),
                                rx.icon("circle-alert", class_name="stroke-zinc-200"),
                            ),
                            class_name="pl-4"
                        ),
                        class_name="flex-row justify-between w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_input_actual_ratio,
                                text(
                                    f"1 : {ReportState.staffing_input_actual_ratio}",
                                    class_name="text-2xl font-bold"
                                ),
                                text(
                                    "1 : ?",
                                    class_name="text-2xl font-bold"
                                )
                            ),
                            calculator("actual_ratio"),
                            class_name="flex-row items-center space-x-2"
                        ),
                        class_name="flex-row justify-center w-full"
                    ),
                    class_name="flex-col space-y-2 p-4 w-full"
                ),
            ),

            # Do you feel like this ratio is safe and appropriate?
            rx.cond(
                ReportState.staffing_select_ratio == "Yes",
                rx.flex(
                    rx.flex(
                        rx.text("Do you feel like this ratio is safe and appropriate?"),
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_select_ratio_appropriate,
                                rx.icon("circle-check-big", class_name="stroke-green-400"),
                                rx.icon("circle-alert", class_name="stroke-zinc-200"),
                            ),
                            class_name="pl-4"
                        ),
                        class_name="flex-row justify-between w-full"
                    ),
                    rx.select(
                        constants_types.STAFFING_SELECT_RATIO_APPROPRIATE,
                        placeholder="- Select -",
                        value=ReportState.staffing_select_ratio_appropriate,
                        position="popper",
                        on_change=ReportState.set_staffing_select_ratio_appropriate,
                        required=True,
                        size="3",
                        width="100%",
                    ),
                    class_name="flex-col p-4 space-y-2 w-full",
                ),
            ),

            # What patient ratio would be safe?
            rx.cond(
                ReportState.staffing_select_ratio_appropriate == "No",
                rx.flex(
                    rx.flex(
                        rx.text("What nurse : patient ratio would be safe?"),
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_input_ideal_ratio,
                                rx.icon("circle-check-big", class_name="stroke-green-400"),
                                rx.icon("circle-alert", class_name="stroke-zinc-200"),
                            ),
                            class_name="pl-4"
                        ),
                        class_name="flex-row justify-between w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_input_ideal_ratio,
                                text(
                                    f"1 : {ReportState.staffing_input_ideal_ratio}",
                                    class_name="text-2xl font-bold"
                                ),
                                text(
                                    "1 : ?",
                                    class_name="text-2xl font-bold"
                                )
                            ),
                            calculator("ideal_ratio"),
                            class_name="flex-row items-center space-x-2"
                        ),
                        class_name="flex-row justify-center w-full"
                    ),
                    class_name="flex-col space-y-2 p-4 w-full"
                ),
            ),

            # How would you rate the average daily workload?
            rx.flex(
                rx.flex(
                    rx.text("How would you rate the average daily workload?"),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_workload,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-alert", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.STAFFING_SELECT_WORKLOAD_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.staffing_select_workload,
                    position="popper",
                    on_change=ReportState.set_staffing_select_workload,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col p-4 space-y-2 w-full",
            ),

            # How would you rate how hospital policy around staffing and workloads affects your work?
            rx.flex(
                rx.flex(
                    rx.text("How do you usually feel at the end of your shift?"),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_rate_workload,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.flex(
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_rate_workload == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_rate_workload(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_rate_workload == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_rate_workload(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_rate_workload == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_rate_workload(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_rate_workload == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_rate_workload(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_rate_workload == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_rate_workload(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),

            # Does your assignment have a charge nurse?
            rx.flex(
                rx.flex(
                    rx.text("Does your assignment have a charge nurse?"),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_charge_present,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-alert", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.STAFFING_SELECT_CHARGE_PRESENT_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.staffing_select_charge_present,
                    position="popper",
                    on_change=ReportState.set_staffing_select_charge_present,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col p-4 space-y-2 w-full",
            ),

            # Does your charge nurse have to take patients?
            rx.cond(
                ReportState.staffing_select_charge_present == "Yes",
                rx.flex(
                    rx.flex(
                        rx.text("Does your charge nurse have to take patients?"),
                        rx.flex(
                            rx.cond(
                                ReportState.staffing_select_charge_assignment,
                                rx.icon("circle-check-big", class_name="stroke-green-400"),
                                rx.icon("circle-alert", class_name="stroke-zinc-200"),
                            ),
                            class_name="pl-4"
                        ),
                        class_name="flex-row justify-between w-full"
                    ),
                    rx.select(
                        constants_types.STAFFING_SELECT_CHARGE_ASSIGNMENT_SELECTIONS,
                        placeholder="- Select -",
                        value=ReportState.staffing_select_charge_assignment,
                        position="popper",
                        on_change=ReportState.set_staffing_select_charge_assignment,
                        required=True,
                        size="3",
                        width="100%",
                    ),
                    class_name="flex-col p-4 space-y-2 w-full",
                ),
            ),

            # Select benefits?
            rx.flex(
                rx.flex(
                    rx.text(
                        """
                        Select support staff available to you as a resource (Optional).
                        """,
                    ),
                    rx.flex(
                        rx.cond(
                            (
                                ReportState.staffing_check_rapid_response
                                | ReportState.staffing_check_behavioral_response
                                | ReportState.staffing_check_transport
                                | ReportState.staffing_check_phlebotomy
                                | ReportState.staffing_check_cvad
                                | ReportState.staffing_check_ivt
                                | ReportState.staffing_check_wocn
                                | ReportState.staffing_check_chaplain
                                | ReportState.staffing_check_educator
                            )
                            ,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_rapid_response,
                                    checked=ReportState.staffing_check_rapid_response,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Rapid Response"),
                                on_click=ReportState.set_staffing_check_rapid_response(~ReportState.staffing_check_rapid_response),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_behavioral_response,
                                    checked=ReportState.staffing_check_behavioral_response,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Behavioral Response"),
                                on_click=ReportState.set_staffing_check_behavioral_response(~ReportState.staffing_check_behavioral_response),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_transport,
                                    checked=ReportState.staffing_check_transport,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Transport"),
                                on_click=ReportState.set_staffing_check_transport(~ReportState.staffing_check_transport),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_phlebotomy,
                                    checked=ReportState.staffing_check_phlebotomy,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Phlebotomy"),
                                on_click=ReportState.set_staffing_check_phlebotomy(~ReportState.staffing_check_phlebotomy),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_cvad,
                                    checked=ReportState.staffing_check_cvad,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("CVAD"),
                                on_click=ReportState.set_staffing_check_cvad(~ReportState.staffing_check_cvad),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_ivt,
                                    checked=ReportState.staffing_check_ivt,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("IV Team"),
                                on_click=ReportState.set_staffing_check_ivt(~ReportState.staffing_check_ivt),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_wocn,
                                    checked=ReportState.staffing_check_wocn,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Wound Care"),
                                on_click=ReportState.set_staffing_check_wocn(~ReportState.staffing_check_wocn),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_chaplain,
                                    checked=ReportState.staffing_check_chaplain,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Chaplain"),
                                on_click=ReportState.set_staffing_check_chaplain(~ReportState.staffing_check_chaplain),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_staffing_check_educator,
                                    checked=ReportState.staffing_check_educator,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Educator"),
                                on_click=ReportState.set_staffing_check_educator(~ReportState.staffing_check_educator),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),                
                        class_name="inline-flex flex-wrap justify-center"
                    ),
                    class_name="flex-col items-center"
                ),
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # How would you rate staffing overall?
            rx.flex(
                rx.flex(
                    rx.text("How would you rate staffing, resources, and workloads overall?"),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_overall,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.flex(
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_overall == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_overall(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_overall == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_overall(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_overall == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_overall(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_overall == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_overall(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_select_overall == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_staffing_select_overall(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),

            # Any comments for your nursing peers about daily patient workloads or staffing?
            rx.flex(
                rx.flex(
                    rx.text(
                        """
                        (Optional) Any comments for your nursing peers
                        about daily patient workloads or staffing?
                        """,
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.staffing_input_comments,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.debounce_input(
                    rx.text_area(
                        value=ReportState.staffing_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_staffing_input_comments,
                        on_blur=ReportState.set_staffing_input_comments,
                        height="10em",
                        size="3",
                        width="100%",
                    ),
                    debounce_timeout=1000,
                ),
                rx.cond(
                    ReportState.staffing_input_comments,
                    rx.cond(
                        ReportState.staffing_input_comments_chars_left < 0,
                        rx.callout(
                            "Please limit response to < 1000 characters!",
                            width="100%",
                            icon="triangle_alert",
                            color_scheme="red",
                            role="alert",
                        ),
                        rx.flex(
                            rx.text(
                                f"{ReportState.staffing_input_comments_chars_left} chars left.",
                            ),
                            width="100%",
                            align_items="center",
                            justify_content="center",
                        ),
                    ),
                    rx.flex(
                        rx.text("1000 character limit."),
                        width="100%",
                        align_items="center",
                        justify_content="center",
                    ),
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),

            # Navigation buttons
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.icon("arrow-left"),
                        rx.text("Back", class_name="font-bold select-none"),
                        on_click=rx.redirect("/report/full-report/assignment"),
                        class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                    ),
                    class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75"
                ),
                rx.flex(
                    rx.flex(
                        rx.text("Submit Report", class_name="font-bold select-none"),
                        on_click=ReportState.handle_submit_staffing,
                        class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                    ),
                    class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75"
                ),
                class_name="flex-row divide-x w-full"
            ),
            class_name="flex-col dark:divide-zinc-500 space-y-2 divide-y w-full",
        ),
        class_name="flex-col border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )

def calculator(label:str) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                rx.icon("pencil", class_name="h-5 w-5"),
                on_click=[
                    ReportState.set_calculator_toggle_ratio(label),
                    ReportState.set_calculator_ratio_value("clear")
                ],
                class_name="flex-row items-center space-x-4 p-2 w-full cursor-pointer"
            )
        ),
        rx.popover.content(
            rx.cond(
                ReportState.calculator_ratio_value,
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.text(
                                f"{ReportState.calculator_ratio_value}",
                                class_name="text-4xl font-bold"
                            ),
                            class_name="flex-row justify-end w-full"
                        ),
                        class_name="flex-row py-4 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("1", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("1"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("2", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("2"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("3", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("3"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("4", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("4"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("5", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("5"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("6", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("6"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("7", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("7"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("8", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("8"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("9", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("9"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("0", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_ratio_value("0"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.icon("delete"),
                            on_click=ReportState.set_calculator_ratio_value("clear"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none w-full active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.popover.close(
                            rx.flex(
                                rx.text("Enter", class_name="text-xl"),
                                on_click=ReportState.set_calculator_ratio_value("enter"),
                                class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none w-full active:bg-zinc-200 transition-colors duration-75"
                            ),
                            class_name="w-full"
                        ),
                        class_name="flex-row w-full"
                    ),
                    class_name="flex-col items-center space-y-2 w-full max-w-xl"
                )
            )
        )
    )
