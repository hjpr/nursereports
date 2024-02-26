
from ..components.c2a import c2a
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.custom import spacer
from ..components.report_progress import progress
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx

@rx.page(
    route="/report/submit/[report_id]/staffing",
    title='Nurse Reports',
    on_load=BaseState.standard_flow('req_login')
)
def staffing_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='1em'),
        rx.flex(
            rx.form(
                rx.vstack(
                    spacer(height='10px'),
                    progress(),
                    spacer(height='10px'),
                    staffing(),
                    ratios(),
                    support(),
                    overall(),
                    comments(),
                    spacer(height='40px'),
                    buttons(),
                    spacer(height='40px'),
                ),
                on_submit=ReportState.handle_submit_staffing
            ),
            padding_x='20px',
            width=['100%', '100%', '600px', '600px', '600px'],
            max_width='1200px',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
        ),
        spacer(height='1em'),
        footer(),
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def description() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Staffing"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.text(
                """Answer questions on workloads and
                staffing ratios depending on if you take patient
                assignments, or work somewhere like a cath lab or
                operating room where ratios aren't applicable.""",
            ),
            width='100%'
        )
    )

def ratios() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Ratios"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.cond(
                ReportState.has_ratios,
                rx.vstack(
                    # STAFFING - PATIENT RATIOS ---------------------
                    rx.vstack(
                        rx.text(
                            "How many patients are you typically assigned?"
                        ),
                        rx.chakra.number_input(
                            value=ReportState.staffing_input_ratio,
                            input_mode='numeric',
                            on_change=ReportState.set_staffing_input_ratio,
                            is_required=True,
                        ),
                        rx.cond(
                            ~ReportState.ratio_is_valid,
                            rx.callout(
                                "A valid number must be entered.",
                                icon='alert_triangle',
                                color_scheme="red",
                                role='alert'
                            )
                        ),
                        width='100%'
                    ),
                    # STAFFING - RATIOS SAFE ------------------------
                    rx.vstack(
                        rx.text(
                            "How often does this ratio feel unsafe?"
                        ),
                        rx.select(
                            ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                            placeholder="- Select -",
                            value=ReportState.staffing_select_ratio_unsafe,
                            on_change=ReportState.set_staffing_select_ratio_unsafe,
                            required=True
                        ),
                        width='100%'
                    ),
                    width='100%'
                )
            ),
            # STAFFING - WORKLOADS ----------------------------------
            rx.vstack(
                rx.text(
                    "How would you rate the average daily workload?"
                ),
                rx.select(
                    ["Overwhelming", "Heavy", "Moderate", "Light"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_workload,
                    on_change=ReportState.set_staffing_select_workload,
                    required=True
                ),
                width='100%'
            ),
            width='100%'
        ),
        width='100%'
    )

def staffing() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Staffing"
                ),
                rx.divider(),
                width='100%'
            ),
            # STAFFING - NURSE STAFFING -----------------------------
            rx.vstack(
                rx.text(
                    "Is the area you work in appropriately staffed with nurses?",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_nursing_shortages,
                    on_change=ReportState.set_staffing_select_nursing_shortages,
                    required=True
                ),
                width='100%'
            ),
            # STAFFING - CNA STAFFING -------------------------------
            rx.vstack(
                rx.text(
                    "Is the area you work in appropriately staffed with nurse aides?",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_aide_shortages,
                    on_change=ReportState.set_staffing_select_aide_shortages,
                    required=True
                ),
                width='100%'
            ),
            # STAFFING - CHARGE -------------------------------------
            rx.vstack(
                rx.text(
                    "Does the area you work in have a charge nurse?"
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_charge_response,
                    on_change=ReportState.set_staffing_select_charge_response,
                    required=True
                ),
                width='100%'
            ),
            # STAFFING - CHARGE PATIENTS ----------------------------
            rx.cond(
                ReportState.has_charge,
                rx.vstack(
                    rx.text(
                        "How often does charge take a patient assignment?"
                    ),
                    rx.select(
                        ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                        placeholder="- Select -",
                        value=ReportState.staffing_select_charge_assignment,
                        on_change=ReportState.set_staffing_select_charge_assignment,
                        required=True
                    ),
                    width='100%'
                )
            ),
            width='100%'
        ),
        width='100%'
    )

def support() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Support"
                ),
                rx.text(
                    "Select support staff available to you as a resource."
                ),
                rx.divider(),
                width='100%'
            ),
            # SUPPORT - SELECT ALL
            rx.hstack(
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_check_transport,
                        checked=ReportState.staffing_check_transport
                    ),
                    rx.text("Transport"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_check_lab,
                        checked=ReportState.staffing_check_lab
                    ),
                    rx.text("Phlebotomy"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_check_cvad,
                        checked=ReportState.staffing_check_cvad
                    ),
                    rx.text("CVAD"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_check_wocn,
                        checked=ReportState.staffing_check_wocn
                    ),
                    rx.text("Wound Care"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_check_chaplain,
                        checked=ReportState.staffing_check_chaplain
                    ),
                    rx.text("Chaplain"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_check_educator,
                        checked=ReportState.staffing_check_educator
                    ),
                    rx.text("Educator"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                width='100%',
                wrap='wrap',
                justify='center'
            ),
            rx.divider(),
            rx.vstack(
                rx.text(
                    "Is support staff readily available to help with tasks?",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_support_available,
                    on_change=ReportState.set_staffing_select_support_available,
                    required=True
                ),
                width='100%'
            ),
            width='100%'
        ),
        width='100%'
    )

def comments() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Comments"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "(Optional) Any comments for your nursing peers about staffing, workloads, or resources?",
                    text_align='center'
                ),
                rx.debounce_input(
                    rx.text_area(
                        ReportState.staffing_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_staffing_input_comments,
                        on_blur=ReportState.set_staffing_input_comments,
                        height='10em'
                    ),
                    debounce_timeout=1000
                ),
                rx.cond(
                    ReportState.staffing_input_comments,
                    # If there is an entry in the comments
                    rx.cond(
                        ReportState.staffing_input_comments_chars_over,
                        # If chars over limit of 500.
                        rx.callout(
                            "Please limit response to < 500 characters!",
                            icon='alert_triangle',
                            color_scheme='red',
                            role='alert'
                        ),
                        # If chars not over limit of 500.
                        rx.text(
                            f"{ReportState.staffing_input_comments_chars_left} chars left.",
                            text_align="center"
                        )
                    ),
                    # If no entry yet in comments
                    rx.text(
                        "500 character limit."
                    )
                ),
                width='100%'
            ),
            width='100%'
        )
    )

def overall() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Grade"
                ),
                rx.text(
                    "How would you grade staffing overall?",
                    text_align='center'
                ),
                rx.divider(),
                width='100%'
            ),
            rx.hstack(
                rx.image(
                    src='/raster/icons/icon_rating_a.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_select_overall("a")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_b.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_select_overall("b")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_c.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_select_overall("c")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_d.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_select_overall("d")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_f.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_select_overall("f")
                ),
                width='100%'
            ),
            rx.cond(
                ~ReportState.staffing_select_overall,
                rx.callout(
                    "Please make a selection.",
                    icon='info'
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.staffing_select_overall.upper()} - {ReportState.staffing_select_overall_description}",
                        color='white',
                        text_align='center',
                    ),
                    background=ReportState.staffing_select_overall_background,
                    border_radius='5px',
                    height='3em',
                    width='100%'
                )
            ),
            width='100%'
        ),
        width='100%'
    )

def buttons() -> rx.Component:
    return rx.center(
        rx.button("Back",
            width='100%',
            on_click=ReportState.report_nav('assignment'),
        ),
        rx.button("Submit",
            width='100%',
            type='submit',
        ),
        width='50%'
    )