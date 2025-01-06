from ..components import (
    flex,
    footer,
    login_protected,
    navbar,
    spacer,
    years_experience
)
from ..components.report_progress import progress
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
        progress(),
        pay(),
        demographics(),
        benefits(),
        compensation(),
        overall(),
        comments(),
        callout(),
        button(),
        class_name="flex-col space-y-8 p-4 w-full max-w-screen-sm"
    )


def pay() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("Pay", class_name="text-xl font-bold"),
            class_name="flex bg-zinc-100 dark:bg-zinc-800 p-4 w-full"
        ),
        flex(
            rx.vstack(
                rx.text("What is your employment type?"),
                rx.select(
                    ["Full-time", "Part-time", "Contract"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_emp_type,
                    on_change=ReportState.set_comp_select_emp_type,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text("Are you paid at an hourly or weekly rate?"),
                rx.select(
                    ["Hourly", "Weekly"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_pay_type,
                    on_change=ReportState.set_comp_select_pay_type,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.comp_select_pay_type,
                rx.cond(
                    ReportState.is_weekly,
                    rx.vstack(
                        rx.text(
                            "Total rate per ",
                            rx.text("week? ", display="inline", font_weight="bold"),
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
                        rx.cond(
                            ReportState.is_pay_invalid,
                            rx.callout(
                                "A valid weekly rate must be entered.",
                                width="100%",
                                icon="triangle_alert",
                                color_scheme="red",
                                role="alert",
                            ),
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            " Base rate per ",
                            rx.text("hour? ", display="inline", font_weight="bold"),
                        ),
                        rx.flex(
                            rx.flex(
                                rx.text(
                                    "$",
                                    class_name="text-xl pr-1"
                                ),
                                rx.input(
                                    id="hourly-digit-1",
                                    size="3",
                                    max_length=1,
                                    class_name="w-9",
                                    on_change=rx.set_focus("hourly-digit-2")
                                ),
                                rx.input(
                                    id="hourly-digit-2",
                                    size="3",
                                    max_length=1,
                                    class_name="w-9",
                                    on_change=rx.set_focus("hourly-digit-3")
                                ),
                                rx.input(
                                    id="hourly-digit-3",
                                    size="3",
                                    max_length=1,
                                    class_name="w-9",
                                    on_change=rx.set_focus("hourly-digit-4")
                                ),
                                rx.text(
                                    ".",
                                    class_name="text-lg pt-4"
                                ),
                                rx.input(
                                    id="hourly-digit-4",
                                    size="3",
                                    max_length=1,
                                    class_name="w-9",
                                    on_change=rx.set_focus("hourly-digit-5")
                                ),
                                rx.input(
                                    id="hourly-digit-5",
                                    size="3",
                                    max_length=1,
                                    class_name="w-9",
                                ),
                                class_name="flex-row items-center space-x-2"
                            ),
                            class_name="flex-row justify-center w-full"
                        ),
                        # rx.chakra.number_input(
                        #     value=ReportState.comp_input_pay_amount,
                        #     input_mode="numeric",
                        #     on_change=ReportState.set_comp_input_pay_amount,
                        #     is_required=True,
                        #     width="100%",
                        # ),
                        rx.cond(
                            ReportState.is_pay_invalid,
                            rx.callout(
                                "A valid hourly rate must be entered.",
                                width="100%",
                                icon="triangle_alert",
                                color_scheme="red",
                                role="alert",
                            ),
                        ),
                        width="100%",
                    ),
                ),
            ),
            rx.vstack(
                rx.text("Do you get extra pay for nights or weekends?"),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_diff_response,
                    on_change=ReportState.set_comp_select_diff_response,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.gets_differential,
                rx.vstack(
                    rx.vstack(
                        rx.text(
                            "(Optional) Extra per hour for ",
                            rx.text("nights? ", display="inline", font_weight="bold"),
                            rx.text("(in $)", display="inline"),
                        ),
                        rx.chakra.number_input(
                            value=ReportState.comp_input_diff_nights,
                            on_change=ReportState.set_comp_input_diff_nights,
                            max=100,
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "(Optional) Extra per hour for ",
                            rx.text(
                                "weekends? ",
                                display="inline",
                                font_weight="bold",
                            ),
                            rx.text("(in $)", display="inline"),
                        ),
                        rx.chakra.number_input(
                            value=ReportState.comp_input_diff_weekends,
                            on_change=ReportState.set_comp_input_diff_weekends,
                            max=100,
                            width="100%",
                        ),
                        width="100%",
                    ),
                    gap="24px",
                    width="100%",
                ),
            ),
            rx.vstack(
                rx.text(
                    """Does your hospital have special incentive pay for
                    certain shifts? (e.g. critical shift pay)""",
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_incentive_response,
                    on_change=ReportState.set_comp_select_incentive_response,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.gets_incentive,
                rx.vstack(
                    rx.text("(Optional) Extra per hour for incentive? (in $)"),
                    rx.chakra.number_input(
                        value=ReportState.comp_input_incentive_amount,
                        on_change=ReportState.set_comp_input_incentive_amount,
                        max_=200,
                        width="100%",
                    ),
                ),
            ),
            rx.vstack(
                rx.text(
                    """Does your hospital pay extra for having certifications?
                    (e.g. CCRN, CWON, RN-BC)""",
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_certifications,
                    on_change=ReportState.set_comp_select_certifications,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            class_name="flex-col dark:divide-zinc-500 space-y-2 p-4 w-full",
        ),
        class_name="flex-col border rounded dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )


def demographics() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Demographics",
            ),
            rx.divider(),
            width="100%",
        ),
        spacer(height="24px"),
        rx.flex(
            rx.vstack(
                rx.text("What shifts do you typically work?"),
                rx.select(
                    ["Day", "Night", "Rotating"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_shift,
                    on_change=ReportState.set_comp_select_shift,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text("On average, how many shifts do you work per week?"),
                rx.select(
                    ["1", "2", "3", "4", "5", "6"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_weekly_shifts,
                    on_change=ReportState.set_comp_select_weekly_shifts,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            # DEMO - TIME AT HOSPITAL AS RN -------------------------
            rx.vstack(
                rx.text("How many years have you worked at this hospital as a RN?"),
                rx.select(
                    years_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_hospital_experience,
                    on_change=ReportState.set_comp_select_hospital_experience,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            # DEMO - TOTAL EXPERIENCE AS RN -------------------------
            rx.vstack(
                rx.text("How many years in total have you worked as a RN?"),
                rx.select(
                    years_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_total_experience,
                    on_change=ReportState.set_comp_select_total_experience,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.is_experience_invalid,
                rx.callout(
                    "Can't have less total years than years at current hospital.",
                    width="100%",
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                ),
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
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
        rx.cond(
            ReportState.comp_has_error,
            rx.callout(
                ReportState.comp_error_message,
                width="100%",
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
            ),
        ),
        width="100%",
    )
