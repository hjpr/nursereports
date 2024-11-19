from ..components import (
    c2a,
    footer,
    leaving_reason,
    login_protected,
    navbar,
    progress,
    spacer,
    unit_specialties,
)
from reflex_motion import motion
from ...states import BaseState, ReportState

import reflex as rx


@rx.page(
    route="/report/full-report/assignment",
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
        c2a(),
        navbar(),
        spacer(height="1em"),
        content(),
        spacer(height="1em"),
        footer(),
        width="100%",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        progress(),
        unit(),
        specialty(),
        culture(),
        burnout(),
        overall(),
        comments(),
        callout(),
        button(),
        spacer(height="48px"),
        gap="24px",
        padding_x="24px",
        width=["100%", "480px", "480px", "480px", "480px"],
        max_width="1200px",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def unit() -> rx.Component:
    return rx.card(
        rx.vstack(rx.heading("Info"), rx.divider(), width="100%"),
        spacer(height="24px"),
        rx.flex(
            rx.vstack(
                rx.text(
                    "Are you submitting a report for a specific unit?",
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_specific_unit,
                    on_change=ReportState.set_assign_select_specific_unit,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.is_unit,
                rx.flex(
                    rx.vstack(
                        rx.text(
                            """What unit are you submitting report for? Select
                            'I don't see my unit' if not present in list.""",
                        ),
                        rx.select(
                            ReportState.hospital_units,
                            placeholder="- Select -",
                            value=ReportState.assign_select_unit,
                            on_change=ReportState.set_assign_select_unit,
                            required=True,
                            size="3",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.cond(
                        ReportState.unit_not_present,
                        rx.flex(
                            rx.flex(
                                rx.text(
                                    """
                                    Enter your unit name as it's commonly known.
                                    """,
                                ),
                                rx.debounce_input(
                                    rx.input(
                                        value=ReportState.assign_input_unit_name,
                                        on_change=ReportState.set_assign_input_unit_name,
                                        required=True,
                                        max_length=40,
                                        size="3",
                                    ),
                                    debounce_timeout=1000,
                                ),
                                rx.cond(
                                    ReportState.name_too_long,
                                    rx.callout(
                                        "Unit name is too long!",
                                        width="100%",
                                        icon="triangle_alert",
                                        color_scheme="red",
                                        role="alert",
                                    ),
                                ),
                                flex_direction="column",
                                gap="8px",
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),
                    rx.vstack(
                        rx.text(
                            "What's the acuity of your unit?",
                        ),
                        rx.select(
                            ["Intensive", "Intermediate", "Floor", "Mixed", "N/A"],
                            placeholder="- Select -",
                            value=ReportState.assign_select_acuity,
                            on_change=ReportState.set_assign_select_acuity,
                            required=True,
                            size="3",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    flex_direction="column",
                    gap="24px",
                    width="100%",
                ),
            ),
            rx.cond(
                ReportState.has_unit & ~ReportState.is_unit,
                rx.flex(
                    rx.vstack(
                        rx.text(
                            """What area or role are you submitting a report for?
                            Select 'I don't see my area or role' if not present in
                            list.""",
                        ),
                        rx.select(
                            ReportState.hospital_areas,
                            placeholder="- Select -",
                            value=ReportState.assign_select_area,
                            on_change=ReportState.set_assign_select_area,
                            required=True,
                            size="3",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.cond(
                        ReportState.area_not_present,
                        rx.flex(
                            rx.text(
                                """
                                Enter your area or role as it's commonly
                                known.
                                """,
                            ),
                            rx.debounce_input(
                                rx.input(
                                    value=ReportState.assign_input_area,
                                    on_change=ReportState.set_assign_input_area,
                                    required=True,
                                    size="3",
                                    max_length=60,
                                ),
                                width="100%",
                                debounce_timeout=1000,
                            ),
                            rx.cond(
                                ReportState.area_too_long,
                                rx.callout(
                                    "Name of area/role too long!",
                                    width="100%",
                                    icon="triangle_alert",
                                    color_scheme="red",
                                    role="alert",
                                ),
                            ),
                            flex_direction="column",
                            gap="8px",
                            width="100%",
                        ),
                    ),
                    flex_direction="column",
                    gap="24px",
                    width="100%",
                ),
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
    )


def specialty() -> rx.Component:
    return rx.card(
        rx.vstack(rx.heading("Specialty"), rx.divider(), width="100%"),
        spacer(height="24px"),
        rx.flex(
            rx.vstack(
                rx.text(
                    """(Optional) What is your unit or area
                    specialty? Select up to three...""",
                ),
                rx.select(
                    unit_specialties,
                    placeholder="- Select -",
                    value=ReportState.assign_select_specialty_1,
                    on_change=ReportState.set_assign_select_specialty_1,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.has_specialty_1,
                rx.vstack(
                    rx.text("(Optional) Additional specialty."),
                    rx.select(
                        unit_specialties,
                        placeholder="- Select -",
                        value=ReportState.assign_select_specialty_2,
                        on_change=ReportState.set_assign_select_specialty_2,
                        size="3",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            rx.cond(
                ReportState.has_specialty_2,
                rx.vstack(
                    rx.text("(Optional) Additional specialty."),
                    rx.select(
                        unit_specialties,
                        placeholder="- Select -",
                        value=ReportState.assign_select_specialty_3,
                        on_change=ReportState.set_assign_select_specialty_3,
                        size="3",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
    )


def culture() -> rx.Component:
    return rx.card(
        rx.vstack(rx.heading("Culture"), rx.divider(), width="100%"),
        spacer(height="24px"),
        rx.flex(
            rx.vstack(
                rx.text(
                    "Are ",
                    rx.text("nurses ", display="inline", font_weight="bold"),
                    rx.text("in your area helpful and supportive?", display="inline"),
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_teamwork_rn,
                    on_change=ReportState.set_assign_select_teamwork_rn,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Are ",
                    rx.text("nurse aides ", display="inline", font_weight="bold"),
                    rx.text("in your area helpful and supportive?", display="inline"),
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_teamwork_na,
                    on_change=ReportState.set_assign_select_teamwork_na,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Do practitioners around you work well with nursing staff?",
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_providers,
                    on_change=ReportState.set_assign_select_providers,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    """
                    Are your inputs into patient care discussions
                    valued?
                    """,
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_contributions,
                    on_change=ReportState.set_assign_select_contributions,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    """
                    Do you feel like you have a positive impact on
                    the outcomes of your patients?
                    """,
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_impact,
                    on_change=ReportState.set_assign_select_impact,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    """
                    Do you feel like management promotes a healthy and
                    positive work environment?
                    """,
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_management,
                    on_change=ReportState.set_assign_select_management,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
    )


def burnout() -> rx.Component:
    return rx.card(
        rx.vstack(rx.heading("Recommendations"), rx.divider(), width="100%"),
        spacer(height="24px"),
        rx.flex(
            rx.vstack(
                rx.text("Do you plan on making career changes in the next year or so?"),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_leaving,
                    on_change=ReportState.set_assign_select_leaving,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                ReportState.is_leaving,
                rx.vstack(
                    rx.text("What's your next move?"),
                    rx.select(
                        leaving_reason,
                        placeholder="- Select -",
                        value=ReportState.assign_select_leaving_reason,
                        on_change=ReportState.set_assign_select_leaving_reason,
                        required=True,
                        size="3",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            rx.vstack(
                rx.text(
                    "Would you recommend a friend or coworker to your current position?"
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_recommend,
                    on_change=ReportState.set_assign_select_recommend,
                    required=True,
                    size="3",
                    width="100%",
                ),
                width="100%",
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
    )


def comments() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(rx.heading("Comments"), rx.divider(), width="100%"),
            spacer(height="24px"),
            rx.text(
                """
                (Optional) Any comments for your nursing peers 
                about culture, management, or environment?
                """,
                text_align="center",
            ),
            rx.debounce_input(
                rx.text_area(
                    ReportState.assign_input_comments,
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
                    ReportState.assign_input_comments_chars_over,
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
            width="100%",
        ),
        width="100%",
    )


def overall() -> rx.Component:
    return rx.card(
        rx.vstack(rx.heading("Grade"), rx.divider(), width="100%"),
        spacer(height="24px"),
        rx.flex(
            rx.text(
                "How would you grade your assignment overall?", text_align="center"
            ),
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
                        on_click=ReportState.set_assign_select_overall("a"),
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
                        on_click=ReportState.set_assign_select_overall("b"),
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
                        on_click=ReportState.set_assign_select_overall("c"),
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
                        on_click=ReportState.set_assign_select_overall("d"),
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
                        on_click=ReportState.set_assign_select_overall("f"),
                    ),
                    initial={"scale": 1},
                    while_tap={"scale": 0.95},
                ),
                flex_direction="row",
                justify_content="space-between",
                width="100%",
            ),
            rx.cond(
                ~ReportState.assign_select_overall,
                rx.callout(
                    "Please make a selection.",
                    width="100%",
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.assign_select_overall.upper()} - {ReportState.assign_select_overall_description}",
                        color="white",
                        text_align="center",
                    ),
                    background=ReportState.assign_select_overall_background,
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
