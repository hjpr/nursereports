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
    route="/report/[report_mode]/assignment",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def assignment_page() -> rx.Component:
    return rx.flex(
        navbar(), content(), footer(), class_name="flex-col items-center w-full"
    )


def content() -> rx.Component:
    return rx.flex(
        assignment(),
        class_name="flex-col items-center space-y-12 px-4 py-14 md:py-20 w-full max-w-screen-sm",
    )


def assignment() -> rx.Component:
    return rx.flex(
        rx.flex(
            text("Assignment", class_name="text-2xl font-bold"),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-6 w-full",
        ),
        flex(
            # Are you submitting a report for a specific unit?
            rx.flex(
                rx.flex(
                    rx.text(
                        "How would you classify where you work? Examples for each are shown below."
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_classify,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.flex(
                    rx.text("Unit - STICU, PACU, 6 NORTH, ED"),
                    rx.text("Area - OR, VIR, CATH LAB"),
                    rx.text("Role - WOUND CARE, ICU TRANSPORT, FLOAT POOL"),
                    class_name="flex-col pl-8 w-full",
                ),
                rx.select(
                    constants_types.ASSIGN_SELECT_CLASSIFY_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.assign_select_classify,
                    position="popper",
                    on_change=ReportState.set_assign_select_classify,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col p-4 space-y-2 w-full",
            ),
            # Context menus for work classification.
            rx.match(
                ReportState.assign_select_classify,
                # What unit are you submitting report for?
                (
                    "Unit",
                    rx.flex(
                        rx.flex(
                            rx.flex(
                                rx.text("What unit are you submitting a report for?"),
                                rx.flex(
                                    rx.cond(
                                        ReportState.assign_select_unit,
                                        rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                        rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                    ),
                                    class_name="pl-4"
                                ),
                                class_name="flex-row justify-between w-full",
                            ),
                            rx.select(
                                ReportState.hospital_units,
                                placeholder="- Select -",
                                value=ReportState.assign_select_unit,
                                position="popper",
                                on_change=ReportState.set_assign_select_unit,
                                required=True,
                                size="3",
                                width="100%",
                            ),
                            class_name="flex-col p-4 space-y-2 w-full",
                        ),
                        rx.cond(
                            ReportState.assign_select_unit == "I don't see my unit",
                            rx.flex(
                                rx.flex(
                                    rx.flex(
                                        rx.text(
                                            "Enter your unit as it's commonly known."
                                        ),
                                        rx.flex(
                                            rx.cond(
                                                ReportState.assign_input_unit,
                                                rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                                rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                            ),
                                            class_name="pl-4"
                                        ),
                                        class_name="flex-row justify-between w-full",
                                    ),
                                    rx.debounce_input(
                                        rx.input(
                                            value=ReportState.assign_input_unit,
                                            on_change=ReportState.set_assign_input_unit,
                                            required=True,
                                            max_length=50,
                                            size="3",
                                        ),
                                        debounce_timeout=1000,
                                    ),
                                    class_name="flex-col p-4 space-y-2 w-full",
                                ),
                                width="100%",
                            ),
                        ),
                        rx.flex(
                            rx.flex(
                                rx.text("What's the acuity of your unit?"),
                                rx.flex(
                                    rx.cond(
                                        ReportState.assign_select_acuity,
                                        rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                        rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                    ),
                                    class_name="pl-4"
                                ),
                                class_name="flex-row justify-between w-full",
                            ),
                            rx.select(
                                constants_types.ASSIGN_SELECT_ACUITY_SELECTIONS,
                                placeholder="- Select -",
                                value=ReportState.assign_select_acuity,
                                position="popper",
                                on_change=ReportState.set_assign_select_acuity,
                                required=True,
                                size="3",
                                width="100%",
                            ),
                            class_name="flex-col p-4 space-y-2 w-full",
                        ),
                        class_name="flex-col divide-y w-full",
                    ),
                ),
                (
                    "Area",
                    rx.flex(
                        # What area are you submitting a report for?
                        rx.flex(
                            rx.flex(
                                rx.text("What area are you submitting a report for?"),
                                rx.flex(
                                    rx.cond(
                                        ReportState.assign_select_area,
                                        rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                        rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                    ),
                                    class_name="pl-4"
                                ),
                                class_name="flex-row justify-between w-full",
                            ),
                            rx.select(
                                ReportState.hospital_areas,
                                placeholder="- Select -",
                                value=ReportState.assign_select_area,
                                position="popper",
                                on_change=ReportState.set_assign_select_area,
                                required=True,
                                size="3",
                                width="100%",
                            ),
                            class_name="flex-col p-4 space-y-2 w-full",
                        ),
                        rx.cond(
                            ReportState.assign_select_area == "I don't see my area",
                            rx.flex(
                                rx.flex(
                                    rx.text("Enter your area as it's commonly known."),
                                    rx.flex(
                                        rx.cond(
                                            ReportState.assign_input_area,
                                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                        ),
                                        class_name="pl-4"
                                    ),
                                    class_name="flex-row justify-between w-full",
                                ),
                                rx.debounce_input(
                                    rx.input(
                                        value=ReportState.assign_input_area,
                                        on_change=ReportState.set_assign_input_area,
                                        required=True,
                                        size="3",
                                        max_length=50,
                                    ),
                                    width="100%",
                                    debounce_timeout=1000,
                                ),
                                class_name="flex-col p-4 space-y-2 w-full",
                            ),
                        ),
                        class_name="flex-col w-full",
                    ),
                ),
                (
                    "Role",
                    rx.flex(
                        # What role are you submitting a report for?
                        rx.flex(
                            rx.flex(
                                rx.text("What role are you submitting a report for?"),
                                rx.flex(
                                    rx.cond(
                                        ReportState.assign_select_role,
                                        rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                        rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                    ),
                                    class_name="pl-4"
                                ),
                                class_name="flex-row justify-between w-full",
                            ),
                            rx.select(
                                ReportState.hospital_roles,
                                placeholder="- Select -",
                                value=ReportState.assign_select_role,
                                position="popper",
                                on_change=ReportState.set_assign_select_role,
                                required=True,
                                size="3",
                                width="100%",
                            ),
                            class_name="flex-col p-4 space-y-2 w-full",
                        ),
                        rx.cond(
                            ReportState.assign_select_role == "I don't see my role",
                            rx.flex(
                                rx.flex(
                                    rx.text("Enter your role as it's commonly known."),
                                    rx.flex(
                                        rx.cond(
                                            ReportState.assign_input_role,
                                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                                        ),
                                        class_name="pl-4"
                                    ),
                                    class_name="flex-row justify-between w-full",
                                ),
                                rx.debounce_input(
                                    rx.input(
                                        value=ReportState.assign_input_role,
                                        on_change=ReportState.set_assign_input_role,
                                        required=True,
                                        size="3",
                                        max_length=50,
                                    ),
                                    width="100%",
                                    debounce_timeout=1000,
                                ),
                                class_name="flex-col p-4 space-y-2 w-full",
                            ),
                        ),
                        class_name="flex-col w-full",
                    ),
                ),
            ),

            # What is your unit or role specialty
            rx.flex(
                rx.flex(
                    rx.text(
                        "Select up to three specialties for your position. (Optional)"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_specialty_1,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.select(
                    ReportState.assign_specialty_1,
                    placeholder="- Select -",
                    value=ReportState.assign_select_specialty_1,
                    position="popper",
                    on_change=ReportState.set_assign_select_specialty_1,
                    size="3",
                    width="100%",
                ),
                rx.select(
                    ReportState.assign_specialty_2,
                    placeholder="- Select -",
                    value=ReportState.assign_select_specialty_2,
                    position="popper",
                    disabled=~ReportState.assign_select_specialty_1,
                    on_change=ReportState.set_assign_select_specialty_2,
                    size="3",
                    width="100%",
                ),
                rx.select(
                    ReportState.assign_specialty_3,
                    placeholder="- Select -",
                    value=ReportState.assign_select_specialty_3,
                    position="popper",
                    disabled=~ReportState.assign_select_specialty_2,
                    on_change=ReportState.set_assign_select_specialty_3,
                    size="3",
                    width="100%",
                ),
                rx.flex(
                    outline_button(
                        "Clear",
                        size="3",
                        on_click=[
                            ReportState.set_assign_select_specialty_1(""),
                            ReportState.set_assign_select_specialty_2(""),
                            ReportState.set_assign_select_specialty_3(""),
                        ],
                    ),
                    class_name="flex-col items-center w-full",
                ),
                class_name="flex-col p-4 space-y-2 w-full",
            ),

            # How is working with other nurses where you are assigned?
            rx.flex(
                rx.flex(
                    rx.text("How is working with other nurses around you?"),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurses,
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
                            ReportState.assign_select_rate_nurses == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurses(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurses == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurses(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurses == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurses(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurses == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurses(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurses == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurses(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),

            # How is working with nurse aides?
            rx.flex(
                rx.flex(
                    rx.text("How is working with the nurse aides around you?"),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurse_aides,
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
                            ReportState.assign_select_rate_nurse_aides == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurse_aides(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurse_aides == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurse_aides(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurse_aides == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurse_aides(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurse_aides == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurse_aides(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_nurse_aides == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_nurse_aides(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            # How is working with the physicians/practitioners where you are assigned?
            rx.flex(
                rx.flex(
                    rx.text(
                        "How is working with the physicians/practitioners around you?"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_physicians,
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
                            ReportState.assign_select_rate_physicians == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_physicians(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_physicians == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_physicians(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_physicians == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_physicians(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_physicians == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_physicians(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_physicians == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_physicians(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            # How is working with your immediate management where you are assigned?
            rx.flex(
                rx.flex(
                    rx.text("How is working with your immediate management?"),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_management,
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
                            ReportState.assign_select_rate_management == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_management(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_management == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_management(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_management == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_management(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_management == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_management(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_rate_management == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_rate_management(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            # Would you recommend a friend or coworker to your current position?
            rx.flex(
                rx.flex(
                    rx.text(
                        "Would you recommend a friend or coworker to your current position?"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_recommend,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-alert", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.select(
                    constants_types.ASSIGN_SELECT_RECOMMEND_SELECTIONS,
                    placeholder="- Select -",
                    value=ReportState.assign_select_recommend,
                    position="popper",
                    on_change=ReportState.set_assign_select_recommend,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col p-4 space-y-2 w-full",
            ),
            # How do you feel about the culture where you are and people you work with overall?
            rx.flex(
                rx.flex(
                    rx.text(
                        "How do you feel about the culture and people you work with overall?"
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_overall,
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
                            ReportState.assign_select_overall == 1,
                            rx.icon("angry", class_name="h-10 w-10 fill-red-400"),
                            rx.icon("angry", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_overall(1),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_overall == 2,
                            rx.icon("frown", class_name="h-10 w-10 fill-orange-400"),
                            rx.icon("frown", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_overall(2),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_overall == 3,
                            rx.icon("meh", class_name="h-10 w-10 fill-yellow-300"),
                            rx.icon("meh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_overall(3),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_overall == 4,
                            rx.icon("smile", class_name="h-10 w-10 fill-green-400"),
                            rx.icon("smile", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_overall(4),
                        class_name="p-4 cursor-pointer",
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_select_overall == 5,
                            rx.icon("laugh", class_name="h-10 w-10 fill-blue-300"),
                            rx.icon("laugh", class_name="h-10 w-10 stroke-zinc-400"),
                        ),
                        on_click=ReportState.set_assign_select_overall(5),
                        class_name="p-4 cursor-pointer",
                    ),
                    class_name="flex-row justify-around w-full",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            # Any comments for your nursing peers about culture, management, or environment?
            rx.flex(
                rx.flex(
                    rx.text(
                        """
                        (Optional) Any comments for your nursing peers 
                        about culture, management, or the environment you work in?
                        """,
                    ),
                    rx.flex(
                        rx.cond(
                            ReportState.assign_input_comments,
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-zinc-200"),
                        ),
                        class_name="pl-4"
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.debounce_input(
                    rx.text_area(
                        value=ReportState.assign_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_assign_input_comments,
                        on_blur=ReportState.set_assign_input_comments,
                        height="10em",
                        size="3",
                        width="100%",
                    ),
                    debounce_timeout=1000,
                ),
                rx.cond(
                    ReportState.assign_input_comments,
                    rx.cond(
                        ReportState.assign_input_comments_chars_left < 0,
                        rx.callout(
                            "Please limit response to < 1000 characters!",
                            width="100%",
                            icon="triangle_alert",
                            color_scheme="red",
                            role="alert",
                        ),
                        rx.flex(
                            rx.text(
                                f"{ReportState.assign_input_comments_chars_left} chars left.",
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
                        on_click=rx.redirect("/report/full-report/compensation"),
                        class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer",
                    ),
                    class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
                ),
                rx.flex(
                    rx.flex(
                        rx.text("Next", class_name="font-bold select-none"),
                        rx.icon("arrow-right"),
                        on_click=ReportState.handle_submit_assignment,
                        class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer",
                    ),
                    class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
                ),
                class_name="flex-row divide-x w-full",
            ),
            class_name="flex-col dark:divide-zinc-500 space-y-2 divide-y w-full",
        ),
        class_name="flex-col border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )


def button() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Go to Staffing",
                rx.icon("arrow-big-right"),
                on_click=ReportState.handle_submit_assignment,
                variant="ghost",
                size="3",
            ),
            align_items="center",
            justify_content="center",
            width="100%",
        ),
        width="100%",
    )


def callout() -> rx.Component:
    return rx.flex(
        rx.cond(
            ReportState.assign_has_error,
            rx.callout(
                ReportState.assign_error_message,
                width="100%",
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
            ),
        ),
        width="100%",
    )
