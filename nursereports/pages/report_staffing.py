
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer
from ..components.report_progress import progress
from ..states.report import ReportState

import reflex as rx

def staffing_page() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='1em'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.form(
                rx.vstack(

                    spacer(height='10px'),

                    progress(),

                    spacer(height='10px'),

                    description(),

                    ratios(),

                    staffing(),

                    support(),

                    comments(),

                    overall(),

                    spacer(height='40px'),

                    buttons(),

                    spacer(height='40px'),

                    spacing='1em'
                ),
                on_submit=ReportState.handle_submit_staffing
            ),
            # STYLING FOR CONTENT CONTAINER
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

        # STYLING FOR BODY CONTAINER
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
                    "Staffing",
                    size='lg'
                ),
                rx.divider(),
                width='100%'
            ),
            rx.text(
                """This section captures information on workloads and
                staffing ratios depending on if you take patient
                assignments, or work somewhere like a cath lab or
                operating room where ratios aren't applicable.""",
            ),
            spacing='2em',
            width='100%'
        )
    )

def ratios() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Ratios",
                    size='md'
                ),
                rx.divider(),
                width='100%'
            ),
            # STAFFING - RATIOS -------------------------------------
            rx.vstack(
                rx.text(
                    "Do you get a set of patients assigned to you each shift?",
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.staffing_ratio_response,
                    variant='filled',
                    on_change=ReportState.set_staffing_ratio_response,
                    is_required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.has_ratios,
                rx.vstack(
                    # STAFFING - AREA -------------------------------
                    rx.text(
                        """Are you staffed to one area, or are you a
                        float?"""
                    ),
                    rx.select(
                    ["Staff", "Float"],
                        placeholder="- Select -",
                        value=ReportState.staffing_ratio_variable,
                        variant='filled',
                        on_change=ReportState.set_staffing_ratio_variable,
                        is_required=True
                    ),
                    width='100%'
                )
            ),
            rx.cond(
                ReportState.same_ratio,
                rx.vstack(
                    # STAFFING - PATIENT RATIOS ---------------------
                    rx.vstack(
                        rx.text(
                            "How many patients are you typically assigned?"
                        ),
                        rx.number_input(
                            value=ReportState.staffing_ratio,
                            variant='filled',
                            input_mode='numeric',
                            on_change=ReportState.set_staffing_ratio,
                            is_required=True,
                        ),
                        rx.cond(
                            ~ReportState.ratio_is_valid,
                            rx.alert(
                                rx.alert_icon(),
                                rx.alert_title(
                                    "A valid number must be entered."
                                ),
                                border_radius='5px'
                            )
                        ),
                        width='100%'
                    ),
                    # STAFFING - RATIOS SAFE ------------------------
                    rx.vstack(
                        rx.box(
                            rx.span("How often does this ratio feel "),
                            rx.span(
                                "unsafe?",
                                font_weight='bold',
                                text_align='center'
                            )
                        ),
                        rx.select(
                            ["Never", "Rarely", "Sometimes", "Often", "Always"],
                            placeholder="- Select -",
                            value=ReportState.staffing_ratio_unsafe,
                            variant='filled',
                            on_change=ReportState.set_staffing_ratio_unsafe,
                            is_required=True
                        ),
                        width='100%'
                    ),
                    spacing='2em',
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
                    value=ReportState.staffing_workload,
                    variant='filled',
                    on_change=ReportState.set_staffing_workload,
                    is_required=True
                ),
                width='100%'
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def staffing() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Staffing",
                    size='md'
                ),
                rx.divider(),
                width='100%'
            ),
            # STAFFING - NURSE STAFFING -----------------------------
            rx.vstack(
                rx.box(
                    rx.span("How often is your area appropriately staffed with "),
                    rx.span(
                        " nurses?",
                        font_weight='bold'
                    ),
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                    placeholder="- Select -",
                    value=ReportState.staffing_nursing_shortages,
                    variant='filled',
                    on_change=ReportState.set_staffing_nursing_shortages,
                    is_required=True
                ),
                width='100%'
            ),
            # STAFFING - CNA STAFFING -------------------------------
            rx.vstack(
                rx.box(
                    rx.span("How often is your area appropriately staffed with "),
                    rx.span(
                        "nurse aides?",
                        font_weight='bold'
                    ),
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.staffing_aide_shortages,
                    variant='filled',
                    on_change=ReportState.set_staffing_aide_shortages,
                    is_required=True
                ),
                width='100%'
            ),
            # STAFFING - CHARGE -------------------------------------
            rx.vstack(
                rx.text(
                    "Does your area have a charge nurse?"
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.staffing_charge_response,
                    variant='filled',
                    on_change=ReportState.set_staffing_charge_response,
                    is_required=True
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
                        value=ReportState.staffing_charge_assignment,
                        variant='filled',
                        on_change=ReportState.set_staffing_charge_assignment,
                        is_required=True
                    ),
                    width='100%'
                )
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def support() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Support",
                    size='md'
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
                        on_change=ReportState.set_staffing_select_transport,
                        is_checked=ReportState.staffing_select_transport
                    ),
                    rx.text("Transport"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_select_lab,
                        is_checked=ReportState.staffing_select_lab
                    ),
                    rx.text("Phlebotomy"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_select_cvad,
                        is_checked=ReportState.staffing_select_cvad
                    ),
                    rx.text("CVAD"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_select_wocn,
                        is_checked=ReportState.staffing_select_wocn
                    ),
                    rx.text("Wound Care"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_select_chaplain,
                        is_checked=ReportState.staffing_select_chaplain
                    ),
                    rx.text("Chaplain"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_staffing_select_educator,
                        is_checked=ReportState.staffing_select_educator
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
                    value=ReportState.staffing_support_available,
                    variant='filled',
                    on_change=ReportState.set_staffing_support_available,
                    is_required=True
                ),
                width='100%'
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def comments() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Comments",
                    size='md'
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "Any comments for your nursing peers about staffing, workloads, and/or available resources?",
                    text_align='center'
                ),
                rx.debounce_input(
                    rx.text_area(
                        ReportState.staffing_comments,
                        placeholder="(Optional) Do not enter personally identifiable information.",
                        on_change=ReportState.set_staffing_comments,
                        on_blur=ReportState.set_staffing_comments,
                        variant='filled',
                        height='10em'
                    ),
                    debounce_timeout=1000
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.staffing_comments,
                # If there is an entry in the comments
                rx.cond(
                    ReportState.staffing_comments_chars_over,
                    # If chars over limit of 500.
                    rx.alert(
                        rx.alert_icon(),
                        rx.alert_title(
                            "Please limit response to < 500 characters!",
                        ),
                        status='error'
                    ),
                    # If chars not over limit of 500.
                    rx.text(
                        f"{ReportState.staffing_comments_chars_left} chars left.",
                        text_align="center"
                    )
                ),
                # If no entry yet in comments
                rx.text(
                    "500 character limit."
                )
            ),
            spacing='2em',
            width='100%'
        )
    )

def overall() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Grade",
                    size='md'
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
                    on_click=ReportState.set_staffing_overall("a")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_b.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_overall("b")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_c.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_overall("c")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_d.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_overall("d")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_f.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_staffing_overall("f")
                ),
                width='100%'
            ),
            rx.cond(
                ~ReportState.staffing_overall,
                rx.alert(
                    rx.alert_icon(),
                    rx.alert_title(
                        "Please make a selection."
                    ),
                    border_radius='5px',
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.staffing_overall.upper()} - {ReportState.staffing_overall_description}",
                        color='white',
                        text_align='center',
                        size='lg'
                    ),
                    background=ReportState.staffing_overall_background,
                    border_radius='5px',
                    height='3em',
                    width='100%'
                )
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def buttons() -> rx.Component:
    return rx.button_group(
        rx.button("Back",
                width='100%',
                on_click=ReportState.report_nav('compensation'),
                is_loading=~rx.State.is_hydrated,
                color_scheme='teal'
        ),
        rx.button("Next",
            width='100%',
            type_='submit',
            is_loading=~rx.State.is_hydrated,
            is_disabled=~ReportState.staffing_can_progress,
            color_scheme='teal'
        )
    )