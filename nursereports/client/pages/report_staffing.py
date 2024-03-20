
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.report_progress import progress
from reflex_motion import motion
from ...states.base_state import BaseState
from ...states.report_state import ReportState

import reflex as rx

@rx.page(
    route="/report/submit/[hosp_id]/staffing",
    title='Nurse Reports',
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def staffing_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='1em'),
        content(),
        spacer(height='1em'),
        footer(),
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        progress(),
        staffing(),
        ratios(),
        support(),
        overall(),
        comments(),
        button(),
        spacer(height='40px'),
        gap='24px',
        padding_x='24px',
        width=['100%', '480px', '480px', '480px', '480px'],
        max_width='1200px',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def staffing() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Staffing"
            ),
            rx.divider(),
            width='100%'
        ),
        spacer(height='24px'),
        rx.flex(
            rx.vstack(
                rx.text(
                    "Do you have enough ",
                    rx.text(
                        "nurses ",
                        display='inline',
                        font_weight='bold'
                    ),
                    rx.text(
                        "each day to ensure reasonable ratios?",
                        display='inline'
                    )
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_nursing_shortages,
                    on_change=ReportState.set_staffing_select_nursing_shortages,
                    required=True,
                    size='3',
                    width='100%'
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "Do you have enough ",
                    rx.text(
                        "nurse aides ",
                        display='inline',
                        font_weight='bold'
                    ),
                    rx.text(
                        "each day to ensure availability when needed?",
                        display='inline'
                    )
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_aide_shortages,
                    on_change=ReportState.set_staffing_select_aide_shortages,
                    required=True,
                    size='3',
                    width='100%'
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "How would you rate the average daily workload?"
                ),
                rx.select(
                    ["Overwhelming", "Heavy", "Moderate", "Light"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_workload,
                    on_change=ReportState.set_staffing_select_workload,
                    required=True,
                    size='3',
                    width='100%'
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "Does the area you work in have a charge nurse?"
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.staffing_select_charge_response,
                    on_change=ReportState.set_staffing_select_charge_response,
                    required=True,
                    size='3',
                    width='100%'
                ),
                width='100%'
            ),
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
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%'
                )
            ),
            flex_direction='column',
            gap='24px',
            width='100%'
        ),
        width='100%'
    )

def ratios() -> rx.Component:
    return rx.cond(
        ReportState.has_ratios,
        rx.card(
            rx.vstack(
                rx.heading(
                    "Ratios"
                ),
                rx.divider(),
                width='100%'
            ),
            spacer(height='24px'),
            rx.flex(
                rx.vstack(
                    rx.text(
                        "How many patients are you typically assigned?"
                    ),
                    rx.chakra.number_input(
                        value=ReportState.staffing_input_ratio,
                        input_mode='numeric',
                        on_change=ReportState.set_staffing_input_ratio,
                        is_required=True,
                        width='100%'
                    ),
                    rx.cond(
                        ~ReportState.ratio_is_valid,
                        rx.callout(
                            "A valid number must be entered.",
                            width='100%',
                            icon='alert_triangle',
                            color_scheme="red",
                            role='alert'
                        )
                    ),
                    width='100%'
                ),
                rx.vstack(
                    rx.text(
                        "How often does this ratio feel unsafe?"
                    ),
                    rx.select(
                        ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                        placeholder="- Select -",
                        value=ReportState.staffing_select_ratio_unsafe,
                        on_change=ReportState.set_staffing_select_ratio_unsafe,
                        required=True,
                        size='3',
                        width='100%'
                    ),
                    width='100%'
                ),
                flex_direction='column',
                gap='24px',
                width='100%'
            ),
            width='100%'
        )
    )

def support() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Support"
            ),
            rx.divider(),
            width='100%'
        ),
        spacer(height='24px'),
        rx.text(
            "Select support staff available to you as a resource.",
            text_align='center'
        ),
        spacer(height='24px'),
        rx.flex(
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                        on_change=ReportState.set_staffing_check_transport,
                        checked=ReportState.staffing_check_transport
                        ),
                        rx.text("Transport"),
                        gap='12px',
                        align_items='center',
                        justify_content='center'
                    ),
                    cursor='pointer',
                    width='100%',
                    on_click=ReportState.set_staffing_check_transport(
                        ~ReportState.staffing_check_transport
                    )
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95}
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                        on_change=ReportState.set_staffing_check_lab,
                        checked=ReportState.staffing_check_lab
                        ),
                        rx.text("Phlebotomy"),
                        gap='12px',
                        align_items='center',
                        justify_content='center'
                    ),
                    cursor='pointer',
                    width='100%',
                    on_click=ReportState.set_staffing_check_lab(
                        ~ReportState.staffing_check_lab
                    )
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95}
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                        on_change=ReportState.set_staffing_check_cvad,
                        checked=ReportState.staffing_check_cvad
                        ),
                        rx.text("CVAD"),
                        gap='12px',
                        align_items='center',
                        justify_content='center'
                    ),
                    cursor='pointer',
                    width='100%',
                    on_click=ReportState.set_staffing_check_cvad(
                        ~ReportState.staffing_check_cvad
                    )
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95}
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                        on_change=ReportState.set_staffing_check_wocn,
                        checked=ReportState.staffing_check_wocn
                        ),
                        rx.text("Wound Care"),
                        gap='12px',
                        align_items='center',
                        justify_content='center'
                    ),
                    cursor='pointer',
                    width='100%',
                    on_click=ReportState.set_staffing_check_wocn(
                        ~ReportState.staffing_check_wocn
                    )
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95}
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                        on_change=ReportState.set_staffing_check_chaplain,
                        checked=ReportState.staffing_check_chaplain
                        ),
                        rx.text("Chaplain"),
                        gap='12px',
                        align_items='center',
                        justify_content='center'
                    ),
                    cursor='pointer',
                    width='100%',
                    on_click=ReportState.set_staffing_check_chaplain(
                        ~ReportState.staffing_check_chaplain
                    )
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95}
            ),
            motion(
                rx.card(
                    rx.flex(
                        rx.checkbox(
                        on_change=ReportState.set_staffing_check_educator,
                        checked=ReportState.staffing_check_educator
                        ),
                        rx.text("Educator"),
                        gap='12px',
                        align_items='center',
                        justify_content='center'
                    ),
                    cursor='pointer',
                    width='100%',
                    on_click=ReportState.set_staffing_check_educator(
                        ~ReportState.staffing_check_educator
                    )
                ),
                initial={"scale": 1},
                while_tap={"scale": 0.95}
            ),
            flex_direction='column',
            gap='12px',
            width='100%'
        ),
        spacer(height='24px'),
        rx.vstack(
            rx.text(
                "Of the selected resources, are they available for help?",
                text_align='center'
            ),
            rx.select(
                ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                placeholder="- Select -",
                value=ReportState.staffing_select_support_available,
                on_change=ReportState.set_staffing_select_support_available,
                required=True,
                size='3',
                width='100%'
            ),
            width='100%'
        ),
        width='100%'
    )

def comments() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Comments"
            ),
            rx.divider(),
            width='100%'
        ),
        spacer(height='24px'),
        rx.flex(
            rx.vstack(
                rx.text(
                    """
                    (Optional) Any comments for your nursing peers 
                    about staffing, workloads, or resources?
                    """,
                ),
                rx.debounce_input(
                    rx.text_area(
                        ReportState.staffing_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_staffing_input_comments,
                        on_blur=ReportState.set_staffing_input_comments,
                        height='10em',
                        size='3',
                        width='100%'
                    ),
                    debounce_timeout=1000
                ),
                rx.cond(
                    ReportState.staffing_input_comments,
                    rx.cond(
                        ReportState.staffing_input_comments_chars_over,
                        rx.callout(
                            "Please limit response to < 1000 characters!",
                            width='100%',
                            icon='alert_triangle',
                            color_scheme='red',
                            role='alert'
                        ),
                        rx.flex(
                            rx.text(
                                f"{ReportState.staffing_input_comments_chars_left} chars left.",
                            ),
                            width='100%',
                            align_items='center',
                            justify_content='center'
                        )
                    ),
                    rx.flex(
                        rx.text(
                            "1000 character limit."
                        ),
                        width='100%',
                        align_items='center',
                        justify_content='center'
                    )
                ),
                width='100%'
            ),
            flex_direction='column',
            gap='24px',
            width='100%'
        )
    )

def overall() -> rx.Component:
    return rx.card(
            rx.vstack(
                rx.heading(
                    "Grade"
                ),
                rx.divider(),
                width='100%'
            ),
            spacer(height='24px'),
            rx.flex(
                rx.text(
                    "How would you grade staffing overall?",
                    text_align='center'
                ),
                rx.flex(
                    motion(
                        rx.image(
                            src='/raster/icons/icon_rating_a.webp',
                            height=['65px', '65px', '75px', '75px', '75px',],
                            width=['65px', '65px', '75px', '75px', '75px',],
                            border_radius='5px',
                            cursor='pointer',
                            on_click=ReportState.set_staffing_select_overall("a")
                        ),
                        initial={"scale": 1},
                        while_tap={"scale": 0.95}   
                    ),
                    motion(
                        rx.image(
                            src='/raster/icons/icon_rating_b.webp',
                            height=['65px', '65px', '75px', '75px', '75px',],
                            width=['65px', '65px', '75px', '75px', '75px',],
                            border_radius='5px',
                            cursor='pointer',
                            on_click=ReportState.set_staffing_select_overall("b")
                        ),
                        initial={"scale": 1},
                        while_tap={"scale": 0.95}   
                    ),
                    motion(
                        rx.image(
                            src='/raster/icons/icon_rating_c.webp',
                            height=['65px', '65px', '75px', '75px', '75px',],
                            width=['65px', '65px', '75px', '75px', '75px',],
                            border_radius='5px',
                            cursor='pointer',
                            on_click=ReportState.set_staffing_select_overall("c")
                        ),
                        initial={"scale": 1},
                        while_tap={"scale": 0.95}   
                    ),
                    motion(
                        rx.image(
                            src='/raster/icons/icon_rating_d.webp',
                            height=['65px', '65px', '75px', '75px', '75px',],
                            width=['65px', '65px', '75px', '75px', '75px',],
                            border_radius='5px',
                            cursor='pointer',
                            on_click=ReportState.set_staffing_select_overall("d")
                        ),
                        initial={"scale": 1},
                        while_tap={"scale": 0.95}   
                    ),
                    motion(
                        rx.image(
                            src='/raster/icons/icon_rating_f.webp',
                            height=['65px', '65px', '75px', '75px', '75px',],
                            width=['65px', '65px', '75px', '75px', '75px',],
                            border_radius='5px',
                            cursor='pointer',
                            on_click=ReportState.set_staffing_select_overall("f")
                        ),
                        initial={"scale": 1},
                        while_tap={"scale": 0.95}   
                    ),
                    flex_direction='row',
                    justify_content='space-between',
                    width='100%'
            ),
            rx.cond(
                ~ReportState.staffing_select_overall,
                rx.callout(
                    "Please make a selection.",
                    width='100%',
                    icon='alert_triangle',
                    color_scheme='red',
                    role='alert'
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.staffing_select_overall.upper()}\
                            - {ReportState.staffing_select_overall_description}",
                        color='white',
                        text_align='center',
                    ),
                    background=ReportState.staffing_select_overall_background,
                    border_radius='5px',
                    height='3em',
                    width='100%'
                )
            ),
            flex_direction='column',
            gap='24px',
            width='100%'
        ),
        width='100%'
    )

def button() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Submit Report",
                rx.icon("arrow-big-right"),
                on_click=ReportState.handle_submit_staffing,
                variant='ghost',
                size='3'
            ),
            align_items='center',
            justify_content='center',
            width='100%',
        ),
        width='100%'
    )

def callout() -> rx.Component:
    return rx.flex(
        rx.cond(
            ReportState.staffing_has_error,
            rx.callout(
                ReportState.staffing_error_message,
                width='100%',
                icon='alert_triangle',
                color_scheme='red',
                role='alert'
            )
        ),
        width='100%'
    )