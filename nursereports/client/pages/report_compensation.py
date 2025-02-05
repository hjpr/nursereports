from ..components import (
    flex,
    footer,
    login_protected,
    navbar,
    text
)
from ...states import (
    BaseState,
    ReportState,
    constants_types
)

import reflex as rx


@rx.page(
    route="/report/[report_mode]/compensation",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def compensation_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center w-full"
    )


def content() -> rx.Component:
    return rx.flex(
        editing(),
        compensation(),
        class_name="flex-col items-center space-y-4 px-4 py-4 md:py-20 w-full max-w-screen-sm",
    )

def editing() -> rx.Component:
    return rx.cond(
        ReportState.mode == "edit",
        rx.callout(
            rx.text(f"You are currently editing a previously submitted report for {ReportState.hospital_info['hosp_name']}"),
            icon="info",
            class_name="w-full"
        )
    )


def compensation() -> rx.Component:
    return rx.flex(
        rx.flex(
            text("Compensation", class_name="text-2xl font-bold"),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-6 w-full"
        ),
        flex(
            
            # What is your employment type?
            rx.flex(
                rx.flex(
                    rx.text("What is your employment type?"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_emp_type,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.COMP_SELECT_EMP_TYPE_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.comp_select_emp_type,
                    position="popper",
                    on_change=ReportState.set_comp_select_emp_type,
                    required=True,
                    size="3",
                    width="100%",
                ),
                id="comp_select_emp_type",
                class_name="flex-col p-4 space-y-2 w-full",
            ),

            # Are you paid at an hourly or weekly rate?
            rx.flex(
                rx.flex(
                    rx.text("Are you paid at an hourly or weekly rate?"),
                    rx.cond(
                        ReportState.comp_select_pay_type,
                        rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                        rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.COMP_SELECT_PAY_TYPE_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.comp_select_pay_type,
                    position="popper",
                    on_change=ReportState.set_comp_select_pay_type,
                    required=True,
                    size="3",
                    width="100%",
                ),
                id="comp_select_pay_type",
                class_name="flex-col p-4 space-y-2 w-full"
            ),

            # Conditional base rate entries
            rx.cond(
                ReportState.comp_select_pay_type,
                rx.flex(
                    rx.cond(
                        ReportState.comp_select_pay_type == "Weekly",
                        rx.flex(
                            rx.flex(
                                rx.text("Base rate per week?"),
                                rx.cond(
                                    ReportState.comp_input_pay_weekly,
                                    rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                    rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                ),
                                class_name="flex-row justify-between w-full"
                            ),
                            rx.flex(
                                rx.flex(
                                    text(f"$ {ReportState.comp_input_pay_weekly} /wk", class_name="text-2xl font-bold"),
                                    calculator("weekly"),
                                    class_name="flex-row items-center space-x-2"
                                ),
                                class_name="flex-row justify-center w-full"
                            ),
                            class_name="flex-col space-y-2 p-4 w-full"
                        )
                    ),
                    rx.cond(
                        ReportState.comp_select_pay_type == "Hourly",
                        rx.flex(
                            rx.flex(
                                rx.text("Base rate per hour?"),
                                rx.cond(
                                    ReportState.comp_input_pay_hourly,
                                    rx.icon("circle-check-big", class_name="stroke-green-400"),
                                    rx.icon("circle-alert", class_name="stroke-zinc-200")
                                ),
                                class_name="flex-row justify-between w-full"
                            ),
                            rx.flex(
                                rx.flex(
                                    text(f"$ {ReportState.comp_input_pay_hourly} /hr", class_name="text-2xl font-bold"),
                                    calculator("hourly"),
                                    class_name="flex-row items-center space-x-2"
                                ),
                                class_name="flex-row justify-center w-full"
                            ),
                            class_name="flex-col space-y-2 p-4 w-full"
                        )
                    )
                )
            ),

            # Night differential per hour?
            rx.flex(
                rx.flex(
                    rx.text("Night differential per hour? (Optional)"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_input_pay_night,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-check-big", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.flex(
                    rx.flex(
                        text(f"$ {ReportState.comp_input_pay_night} /hr", class_name="text-2xl font-bold"),
                        calculator("night"),
                        class_name="flex-row items-center space-x-2"
                    ),
                    class_name="flex-row justify-center w-full"
                ),
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # Weekend differential per hour?
            rx.flex(
                rx.flex(
                    rx.text("Weekend differential per hour? (Optional)"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_input_pay_weekend,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-check-big", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.flex(
                    rx.flex(
                        text(f"$ {ReportState.comp_input_pay_weekend} /hr", class_name="text-2xl font-bold"),
                        calculator("weekend"),
                        class_name="flex-row items-center space-x-2"
                    ),
                    class_name="flex-row justify-center w-full"
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),

            # Weekend night differential per hour?
            rx.flex(
                rx.flex(
                    rx.text("Weekend night differential per hour? (Optional)"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_input_pay_weekend_night,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-check-big", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.flex(
                    rx.flex(
                        text(f"$ {ReportState.comp_input_pay_weekend_night} /hr", class_name="text-2xl font-bold"),
                        calculator("weekend_night"),
                        class_name="flex-row items-center space-x-2"
                    ),
                    class_name="flex-row justify-center w-full"
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),

            # What shifts do you work?
            rx.flex(
                rx.flex(
                    rx.text("What shifts do you work?"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_shift,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.COMP_SELECT_SHIFT_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.comp_select_shift,
                    position="popper",
                    on_change=ReportState.set_comp_select_shift,
                    required=True,
                    size="3",
                    width="100%",
                ),
                id="comp_select_shift",
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # How many shifts do you work per week on average?
            rx.flex(
                rx.flex(
                    rx.text("How many shifts do you work per week on average?"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_weekly_shifts,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.COMP_SELECT_WEEKLY_SHIFTS_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.comp_select_weekly_shifts,
                    position="popper",
                    on_change=ReportState.set_comp_select_weekly_shifts,
                    required=True,
                    size="3",
                    width="100%",
                ),
                id="comp_select_weekly_shifts",
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # How many years have you worked at this hospital as an RN?
            rx.flex(
                rx.flex(
                    rx.text("How many years have you worked at this hospital as an RN?"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_hospital_experience,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    constants_types.COMP_SELECT_HOSPITAL_EXPERIENCE,
                    placeholder="- Select -",
                    value=ReportState.comp_select_hospital_experience,
                    position="popper",
                    on_change=ReportState.set_comp_select_hospital_experience,
                    required=True,
                    size="3",
                    width="100%",
                ),
                id="comp_select_hospital_experience",
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # How many years in total have you worked as an RN?
            rx.flex(
                rx.flex(
                    rx.text("How many years in total have you worked as an RN?"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_total_experience,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ReportState.years_total_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_total_experience,
                    position="popper",
                    on_change=ReportState.set_comp_select_total_experience,
                    required=True,
                    size="3",
                    disabled=~ReportState.comp_select_hospital_experience,
                    width="100%",
                ),
                id="comp_select_total_experience",
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # Select benefits that are offered to you
            rx.flex(
                rx.flex(
                    rx.text("Select benefits that are offered to you. (Optional)"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_check_benefit_pto,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-check-big", class_name="stroke-zinc-200"),
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
                                    on_change=ReportState.set_comp_check_benefit_pto,
                                    checked=ReportState.comp_check_benefit_pto,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Paid Time Off"),
                                on_click=ReportState.set_comp_check_benefit_pto(~ReportState.comp_check_benefit_pto),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_comp_check_benefit_parental,
                                    checked=ReportState.comp_check_benefit_parental,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Parental Leave"),
                                on_click=ReportState.set_comp_check_benefit_parental(~ReportState.comp_check_benefit_parental),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_comp_check_benefit_insurance,
                                    checked=ReportState.comp_check_benefit_insurance,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Health Insurance"),
                                on_click=ReportState.set_comp_check_benefit_insurance(~ReportState.comp_check_benefit_insurance),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_comp_check_benefit_retirement,
                                    checked=ReportState.comp_check_benefit_retirement,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("401k/Retirement"),
                                on_click=ReportState.set_comp_check_benefit_retirement(~ReportState.comp_check_benefit_retirement),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_comp_check_benefit_tuition,
                                    checked=ReportState.comp_check_benefit_tuition,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Tuition Assistance"),
                                on_click=ReportState.set_comp_check_benefit_tuition(~ReportState.comp_check_benefit_tuition),
                                class_name="flex-row flex-nowrap items-center space-x-2 cursor-pointer"
                            ),
                            class_name="flex-row p-4"
                        ),
                        rx.flex(
                            rx.flex(
                                rx.checkbox(
                                    on_change=ReportState.set_comp_check_benefit_reimbursement,
                                    checked=ReportState.comp_check_benefit_reimbursement,
                                    class_name="cursor-pointer"
                                ),
                                rx.text("Certification Reimbursement"),
                                on_click=ReportState.set_comp_check_benefit_reimbursement(~ReportState.comp_check_benefit_reimbursement),
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

            # How would you grade compensation overall?
            rx.flex(
                rx.flex(
                    rx.text("How would you rate your pay and benefits overall?"),
                    rx.cond(
                        ReportState.comp_select_overall,
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.flex(
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_overall == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_comp_select_overall(1),
                        class_name="p-4 cursor-pointer"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_overall == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_comp_select_overall(2),
                        class_name="p-4 cursor-pointer"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_overall == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_comp_select_overall(3),
                        class_name="p-4 cursor-pointer"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_overall == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_comp_select_overall(4),
                        class_name="p-4 cursor-pointer"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_select_overall == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_comp_select_overall(5),
                        class_name="p-4 cursor-pointer"
                    ),
                    class_name="flex-row justify-around w-full"
                ),
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # Comments for your nursing peers about pay or benefits?
            rx.flex(
                rx.flex(
                    rx.text("Comments or additional info for your nursing peers about pay or benefits? (Optional)"),
                    rx.flex(
                        rx.cond(
                            ReportState.comp_input_comments,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-check-big", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.debounce_input(
                    rx.text_area(
                        value=ReportState.comp_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_comp_input_comments,
                        on_blur=ReportState.set_comp_input_comments,
                        height="10em",
                        size="3",
                        width="100%",
                    ),
                    debounce_timeout=1000,
                ),
                rx.cond(
                    ReportState.comp_input_comments,
                    rx.cond(
                        ReportState.comp_comments_chars_left < 0,
                        rx.callout(
                            "Please limit response to < 1000 characters!",
                            width="100%",
                            icon="triangle_alert",
                            color_scheme="red",
                            role="alert",
                        ),
                        rx.flex(
                            rx.text(
                                f"{ReportState.comp_comments_chars_left} chars left.",
                                text_align="center",
                            ),
                            justify_content="center",
                            width="100%",
                        ),
                    ),
                    rx.flex(
                        rx.text("1000 character limit.", text_align="center"),
                        justify_content="center",
                        width="100%",
                    ),
                ),
                class_name="flex-col space-y-2 p-4 w-full"
            ),

            # Navigation buttons
            rx.cond(
                ReportState.user_is_loading,
                rx.flex(
                    rx.icon("loader-circle", class_name="animate-spin"),
                    class_name="flex-row items-center justify-center p-4 cursor-disabled"
                ),
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.icon("arrow-left"),
                            rx.text("Back", class_name="font-bold select-none"),
                            on_click=rx.redirect(f"/report/{ReportState.mode}/overview"),
                            class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                        ),
                        class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("Next", class_name="font-bold select-none"),
                            rx.icon("arrow-right"),
                            on_click=[
                                ReportState.set_user_is_loading(True),
                                ReportState.handle_submit_compensation,
                                ReportState.set_user_is_loading(False)
                            ],
                            class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                        ),
                        class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75"
                    ),
                    class_name="flex-row divide-x w-full"
                ),
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
                    ReportState.set_input_calculator(label),
                    ReportState.set_calculator_pay_value("clear")
                ],
                class_name="flex-row items-center space-x-4 p-2 w-full cursor-pointer"
            )
        ),
        rx.popover.content(
            rx.cond(
                ReportState.input_calculator,
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.text("$", class_name="text-4xl font-bold"),
                        ),
                        rx.flex(
                            rx.text(
                                f"{ReportState.calculator_pay_value}",
                                class_name="text-4xl font-bold"
                            ),
                            class_name="flex-row justify-end w-full"
                        ),
                        class_name="flex-row py-4 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("1", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("1"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("2", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("2"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("3", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("3"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("4", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("4"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("5", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("5"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("6", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("6"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("7", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("7"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("8", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("8"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.text("9", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("9"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.flex(
                            rx.text("0", class_name="px-2 text-2xl"),
                            on_click=ReportState.set_calculator_pay_value("0"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none active:bg-zinc-200 transition-colors duration-75"
                        ),
                        rx.flex(
                            rx.icon("delete"),
                            on_click=ReportState.set_calculator_pay_value("clear"),
                            class_name="flex-col items-center justify-center border rounded p-3 cursor-pointer select-none w-full active:bg-zinc-200 transition-colors duration-75"
                        ),
                        class_name="flex-row space-x-2 w-full"
                    ),
                    rx.flex(
                        rx.popover.close(
                            rx.flex(
                                rx.text("Enter", class_name="text-xl"),
                                on_click=ReportState.set_calculator_pay_value("enter"),
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