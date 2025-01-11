from ..components import (
    flex,
    footer,
    login_protected,
    navbar,
    spacer,
    text
)
from reflex_motion import motion
from ...states.base_state import BaseState
from ...states.report_state import ReportState

import reflex as rx


@rx.page(
    route="/report/full-report/compensation",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def compensation_page() -> rx.Component:
    return flex(
        navbar(),
        spacer(height="1em"),
        content(),
        spacer(height="1em"),
        footer(),
        class_name="flex-col items-center w-full"
    )


def content() -> rx.Component:
    return rx.flex(
        pay(),
        benefits(),
        compensation(),
        overall(),
        comments(),
        callout(),
        button(),
        class_name="flex-col items-center space-y-12 px-4 py-12 w-full max-w-screen-sm",
    )


def pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            text("Compensation", class_name="text-2xl font-bold"),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-4 w-full"
        ),
        flex(
            # What is your employment type?
            rx.flex(
                rx.flex(
                    rx.text("What is your employment type?"),
                    rx.cond(
                        ReportState.comp_select_emp_type,
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ["Full-time", "Part-time", "Contract"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_emp_type,
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
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ["Hourly", "Weekly"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_pay_type,
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
                                    rx.flex(
                                        rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                                        class_name="pl-4"
                                    ),
                                    rx.flex(
                                        rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                                        class_name="pl-4"
                                    )
                                ),
                                class_name="flex-row justify-between w-full"
                            ),
                            rx.flex(
                                rx.flex(
                                    rx.text(
                                        "$",
                                        class_name="text-xl pr-1"
                                    ),
                                    rx.input(
                                        id="weekly-digit-1",
                                        size="3",
                                        class_name="w-9",
                                        on_change=rx.set_focus("weekly-digit-2")
                                    ),
                                    rx.input(
                                        id="weekly-digit-2",
                                        size="3",
                                        class_name="w-9",
                                        on_change=rx.set_focus("weekly-digit-3")
                                    ),
                                    rx.input(
                                        id="weekly-digit-3",
                                        size="3",
                                        class_name="w-9",
                                        on_change=rx.set_focus("weekly-digit-4")
                                    ),
                                    rx.input(
                                        id="weekly-digit-4",
                                        size="3",
                                        class_name="w-9",
                                    ),
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
                                    rx.icon("circle", class_name="stroke-zinc-200")
                                ),
                                class_name="flex-row justify-between w-full"
                            ),
                            rx.flex(
                                rx.flex(
                                    rx.text(
                                        "$",
                                        class_name="text-xl pr-1"
                                    ),
                                    rx.input(
                                        id="hourly-dollars",
                                        size="3",
                                        max_length=3,
                                        pattern="^[0-9]+$",
                                        class_name="w-14",
                                    ),
                                    rx.text(
                                        ".",
                                        class_name="text-lg pt-4"
                                    ),
                                    rx.input(
                                        id="hourly-cents",
                                        size="3",
                                        max_length=2,
                                        pattern="[0-9]+",
                                        class_name="w-14",
                                    ),
                                    class_name="flex-row items-center space-x-2"
                                ),
                                class_name="flex-row justify-center w-full"
                            ),
                            class_name="flex-col space-y-2 p-4 w-full"
                        )
                    )
                )
            ),
            rx.flex(
                rx.text(
                    "Night differential per hour? (Optional)"
                ),
                rx.flex(
                    rx.flex(
                        rx.text(
                            "$",
                            class_name="text-xl pr-1"
                        ),
                        rx.input(
                            id="nights-digit-1",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                            on_change=rx.set_focus("nights-digit-2")
                        ),
                        rx.input(
                            id="nights-digit-2",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                            on_change=rx.set_focus("nights-digit-3")
                        ),
                        rx.text(
                            ".",
                            class_name="text-lg pt-4"
                        ),
                        rx.input(
                            id="nights-digit-3",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                            on_change=rx.set_focus("nights-digit-4")
                        ),
                        rx.input(
                            id="nights-digit-4",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                        ),
                        class_name="flex-row items-center space-x-2"
                    ),
                    class_name="flex-col items-center w-full"
                ),
                class_name="flex-col space-y-2 p-4 w-full"
            ),
            rx.flex(
                rx.text(
                    "Weekend differential per hour? (Optional)"
                ),
                rx.flex(
                    rx.flex(
                        rx.text(
                            "$",
                            class_name="text-xl pr-1"
                        ),
                        rx.input(
                            id="weekends-digit-1",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                            on_change=rx.set_focus("weekends-digit-2")
                        ),
                        rx.input(
                            id="weekends-digit-2",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                            on_change=rx.set_focus("weekends-digit-3")
                        ),
                        rx.text(
                            ".",
                            class_name="text-lg pt-4"
                        ),
                        rx.input(
                            id="weekends-digit-3",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                            on_change=rx.set_focus("weekends-digit-4")
                        ),
                        rx.input(
                            id="weekends-digit-4",
                            size="3",
                            max_length=1,
                            class_name="w-9",
                        ),
                        class_name="flex-row items-center space-x-2"
                    ),
                    class_name="flex-col items-center w-full"
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            # What shifts do you work?
            rx.flex(
                rx.flex(
                    rx.text("What shifts do you work?"),
                    rx.cond(
                        ReportState.comp_select_shift,
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ["Day", "Night", "Rotating"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_shift,
                    on_change=ReportState.set_comp_select_shift,
                    required=True,
                    size="3",
                    width="100%",
                ),
                id="comp_select_shift",
                class_name="flex-col space-y-2 p-4 w-full"
            ),
            # How many shifts do you work per week?
            rx.flex(
                rx.flex(
                    rx.text("How many shifts do you work per week?"),
                    rx.cond(
                        ReportState.comp_select_weekly_shifts,
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ["1", "2", "3", "4", "5"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_weekly_shifts,
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
                    rx.cond(
                        ReportState.comp_select_hospital_experience,
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ReportState.years_hospital_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_hospital_experience,
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
                    rx.cond(
                        ReportState.comp_select_total_experience,
                        rx.flex(
                            rx.icon("circle-check-big", class_name="h-6 w-6 stroke-green-400"),
                            class_name="pl-4"
                        ),
                        rx.flex(
                            rx.icon("circle", class_name="h-6 w-6 stroke-zinc-200"),
                            class_name="pl-4"
                        )
                    ),
                    class_name="flex-row justify-between w-full"
                ),
                rx.select(
                    ReportState.years_total_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_total_experience,
                    on_change=ReportState.set_comp_select_total_experience,
                    required=True,
                    size="3",
                    disabled=~ReportState.comp_select_hospital_experience,
                    width="100%",
                ),
                id="comp_select_total_experience",
                class_name="flex-col space-y-2 p-4 w-full"
            ),
            class_name="flex-col dark:divide-zinc-500 space-y-2 divide-y w-full",
        ),
        class_name="flex-col border rounded dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )

def benefits() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Benefits",
            ),
            rx.divider(),
            width="100%",
        ),
        spacer(height="24px"),
        rx.text(
            """
            Select all the benefits that are offered for your
            position.
            """,
            text_align="center",
        ),
        spacer(height="24px"),
        rx.flex(
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                            on_change=ReportState.set_comp_check_benefit_pto,
                            checked=ReportState.comp_check_benefit_pto,
                        ),
                        rx.text("PTO"),
                        gap="12px",
                        align_items="center",
                        justify_content="center",
                    ),
                    cursor="pointer",
                    width="100%",
                    on_click=ReportState.set_comp_check_benefit_pto(
                        ~ReportState.comp_check_benefit_pto
                    ),
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95},
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                            on_change=ReportState.set_comp_check_benefit_parental,
                            checked=ReportState.comp_check_benefit_parental,
                        ),
                        rx.text("Parental Leave"),
                        gap="12px",
                        align_items="center",
                        justify_content="center",
                    ),
                    cursor="pointer",
                    width="100%",
                    on_click=ReportState.set_comp_check_benefit_parental(
                        ~ReportState.comp_check_benefit_parental
                    ),
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95},
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                            on_change=ReportState.set_comp_check_benefit_insurance,
                            checked=ReportState.comp_check_benefit_insurance,
                        ),
                        rx.text("Insurance"),
                        gap="12px",
                        align_items="center",
                        justify_content="center",
                    ),
                    cursor="pointer",
                    width="100%",
                    on_click=ReportState.set_comp_check_benefit_insurance(
                        ~ReportState.comp_check_benefit_insurance
                    ),
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95},
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                            on_change=ReportState.set_comp_check_benefit_retirement,
                            checked=ReportState.comp_check_benefit_retirement,
                        ),
                        rx.text("Retirement"),
                        gap="12px",
                        align_items="center",
                        justify_content="center",
                    ),
                    cursor="pointer",
                    width="100%",
                    on_click=ReportState.set_comp_check_benefit_retirement(
                        ~ReportState.comp_check_benefit_retirement
                    ),
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95},
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                            on_change=ReportState.set_comp_check_benefit_tuition,
                            checked=ReportState.comp_check_benefit_tuition,
                        ),
                        rx.text("Tuition Aid"),
                        gap="12px",
                        align_items="center",
                        justify_content="center",
                    ),
                    cursor="pointer",
                    width="100%",
                    on_click=ReportState.set_comp_check_benefit_tuition(
                        ~ReportState.comp_check_benefit_tuition
                    ),
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95},
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                            on_change=ReportState.set_comp_check_benefit_pro_dev,
                            checked=ReportState.comp_check_benefit_pro_dev,
                        ),
                        rx.text("Professional Development"),
                        gap="12px",
                        align_items="center",
                        justify_content="center",
                    ),
                    cursor="pointer",
                    width="100%",
                    on_click=ReportState.set_comp_check_benefit_pro_dev(
                        ~ReportState.comp_check_benefit_pro_dev
                    ),
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95},
            ),
            flex_direction="column",
            gap="12px",
            width="100%",
        ),
        width="100%",
    )


def compensation() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Compensation",
            ),
            rx.divider(),
            width="100%",
        ),
        spacer(height="24px"),
        rx.vstack(
            rx.vstack(
                rx.text(
                    """Is your overall pay and benefits package generally
                    enough to keep you satisfied in your current role?""",
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_comp_adequate,
                    on_change=ReportState.set_comp_select_comp_adequate,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def comments() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Comments",
            ),
            rx.divider(),
            width="100%",
        ),
        spacer(height="24px"),
        rx.vstack(
            rx.vstack(
                rx.text(
                    "(Optional) Any comments for your nursing peers about pay or benefits?"
                ),
                rx.debounce_input(
                    rx.text_area(
                        ReportState.comp_input_comments,
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
                        ReportState.comp_comments_chars_over,
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
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def overall() -> rx.Component:
    return rx.card(
        rx.vstack(rx.heading("Grade"), rx.divider(), width="100%"),
        spacer(height="24px"),
        rx.flex(
            rx.text("How would you grade compensation overall?", text_align="center"),
            rx.flex(
                motion(
                    rx.image(
                        src="/raster/icons/icon_rating_a.webp",
                        height=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        width=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        border_radius="5px",
                        cursor="pointer",
                        on_click=ReportState.set_comp_select_overall("a"),
                    ),
                    initial={"scale": 1},
                    while_tap={"scale": 0.95},
                ),
                motion(
                    rx.image(
                        src="/raster/icons/icon_rating_b.webp",
                        height=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        width=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        border_radius="5px",
                        cursor="pointer",
                        on_click=ReportState.set_comp_select_overall("b"),
                    ),
                    initial={"scale": 1},
                    while_tap={"scale": 0.95},
                ),
                motion(
                    rx.image(
                        src="/raster/icons/icon_rating_c.webp",
                        height=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        width=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        border_radius="5px",
                        cursor="pointer",
                        on_click=ReportState.set_comp_select_overall("c"),
                    ),
                    initial={"scale": 1},
                    while_tap={"scale": 0.95},
                ),
                motion(
                    rx.image(
                        src="/raster/icons/icon_rating_d.webp",
                        height=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        width=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        border_radius="5px",
                        cursor="pointer",
                        on_click=ReportState.set_comp_select_overall("d"),
                    ),
                    initial={"scale": 1},
                    while_tap={"scale": 0.95},
                ),
                motion(
                    rx.image(
                        src="/raster/icons/icon_rating_f.webp",
                        height=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        width=[
                            "65px",
                            "65px",
                            "75px",
                            "75px",
                            "75px",
                        ],
                        border_radius="5px",
                        cursor="pointer",
                        on_click=ReportState.set_comp_select_overall("f"),
                    ),
                    initial={"scale": 1},
                    while_tap={"scale": 0.95},
                ),
                flex_direction="row",
                justify_content="space-between",
                width="100%",
            ),
            rx.cond(
                ~ReportState.comp_select_overall,
                rx.callout(
                    "Please make a selection.",
                    width="100%",
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.comp_select_overall.upper()} - {ReportState.comp_overall_description}",
                        color="white",
                        text_align="center",
                    ),
                    background=ReportState.comp_overall_background,
                    border_radius="5px",
                    height="3em",
                    width="100%",
                ),
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
    )


def button() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Go to Assignment",
                rx.icon("arrow-big-right"),
                on_click=ReportState.handle_submit_compensation,
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
        width="100%",
    )
