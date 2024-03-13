
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.lists import unit_specialties
from ..components.navbar import navbar
from ..components.report_progress import progress
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx

@rx.page(
        route="/report/submit/[hosp_id]/assignment",
        title="Nurse Reports",
        on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def assign_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        rx.flex(
            rx.form(
                rx.vstack(
                    spacer(height='10px'),
                    progress(),
                    spacer(height='10px'),
                    unit(),
                    specialty(),
                    culture(),
                    burnout(),   
                    overall(),
                    comments(),
                    spacer(height='40px'),
                    buttons(),
                    spacer(height='40px'),
                ),
                on_submit=ReportState.handle_submit_assign
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
                    "Assignment"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Answer questions related to culture and management,
                    as well as giving you a chance to freely detail the experience
                    you've had while working your area at the end.""",
                ),
                width='100%'
            ),
            width='100%'
        ),
        width='100%'
    )

def unit() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Info"
                ),
                rx.divider(),
                width='100%'
            ),
            # UNIT - SUBMIT FOR UNIT? -------------------------------
            rx.vstack(
                rx.text(
                    "Are you submitting a report for a specific unit?",
                    text_align='center'
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_specific_unit,
                    on_change=ReportState.set_assign_select_specific_unit,
                    required=True
                ),
                width='100%'
            ),
            # UNIT - IF REPORTING SPECIFIC UNIT ---------------------
            rx.cond(
                ReportState.is_unit,
                rx.vstack(
                    # UNIT - UNIT SELECTION -------------------------
                    rx.vstack(
                        rx.text(
                            """What unit are you submitting report for? Select
                            'I don't see my unit' if not present in list.""",
                            text_align='center'
                        ),
                        rx.select(
                            ReportState.hospital_units,
                            placeholder="- Select -",
                            value=ReportState.assign_select_unit,
                            on_change=ReportState.set_assign_select_unit,
                            required=True
                        ),
                        width='100%'
                    ),
                    # UNIT - IF UNIT NOT PRESENT DROPDOWN -----------
                    rx.cond(
                        ReportState.unit_not_present,
                        rx.vstack(
                            # ASSIGNMENT - UNIT NAME ----------------
                            rx.vstack(
                                rx.text(
                                    """Enter your unit name as it's commonly known
                                    around your hospital.""",
                                    text_align='center'
                                ),
                                rx.debounce_input(
                                    rx.input(
                                        value=ReportState.assign_input_unit_name,
                                        on_change=ReportState.set_assign_input_unit_name,
                                        required=True
                                    ),
                                    debounce_timeout=1000
                                ),
                                rx.cond(
                                    ReportState.name_too_long,
                                    rx.callout(
                                        "Invalid unit name. Too long!",
                                        icon="alert_triangle",
                                        color_scheme="red",
                                        role="alert"
                                    )
                                ),
                                width='100%'
                            ),
                            width='100%'
                        )
                    ),
                    # UNIT - ACUITY ---------------------------------
                    rx.vstack(
                        rx.text(
                            "What's the acuity of your unit?",
                            text_align='center'
                        ),
                        rx.select(
                            ["Intensive", "Intermediate", "Floor", "N/A"],
                            placeholder="- Select -",
                            value=ReportState.assign_select_acuity,
                            on_change=ReportState.set_assign_select_acuity,
                            required=True
                        ),
                        width='100%'
                    ),
                    width='100%'
                )
            ),
            # UNIT - IF NOT REPORTING SPECIFIC UNIT -----------------
            rx.cond(
                ReportState.has_unit & ~ReportState.is_unit,
                rx.vstack(
                    rx.vstack(
                        rx.text(
                            """What area or role are you submitting a report for?
                            Select 'I don't see my area or role' if not present in
                            list.""",
                            text_align='center'
                        ),
                        rx.select(
                            ReportState.hospital_areas,
                            placeholder="- Select -",
                            value=ReportState.assign_select_area,
                            on_change=ReportState.set_assign_select_area,
                            required=True
                        ),
                        width='100%'
                    ),
                    rx.cond(
                        ReportState.area_not_present,
                        rx.vstack(
                            rx.text(
                                """Enter your area or role as it's commonly
                                known around your hospital.""",
                                text_align='center'
                            ),
                            rx.debounce_input(
                                rx.input(
                                    value=ReportState.assign_input_area,
                                    on_change=ReportState.set_assign_input_area
                                ),
                                debounce_timeout=1000
                            ),
                            width='100%'
                        )
                    ),
                    width='100%'
                )
            ),
            width='100%'
        ),
        width="100%"
    )

def specialty() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Specialty"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.vstack(
                    rx.text(
                        """(Optional) What is your unit or area
                        specialty? Select up to three...""",
                        text_align='center'
                    ),
                    rx.select(
                        unit_specialties,
                        placeholder="- Select -",
                        value=ReportState.assign_select_specialty_1,
                        on_change=ReportState.set_assign_select_specialty_1,
                    ),
                    width='100%'
                ),
                rx.cond(
                    ReportState.has_specialty_1,
                    rx.vstack(
                        rx.text(
                            "(Optional) Additional specialty."
                        ),
                        rx.select(
                            unit_specialties,
                            placeholder="- Select -",
                            value=ReportState.assign_select_specialty_2,
                            on_change=ReportState.set_assign_select_specialty_2,
                        ),
                        width='100%'
                    )
                ),
                rx.cond(
                    ReportState.has_specialty_2,
                    rx.vstack(
                        rx.text(
                            "(Optional) Additional specialty."
                        ),
                        rx.select(
                            unit_specialties,
                            placeholder="- Select -",
                            value=ReportState.assign_select_specialty_3,
                            on_change=ReportState.set_assign_select_specialty_3,
                        ),
                        width='100%' 
                    )
                ),
                width='100%'
            ),
            width='100%'
        ),
        width='100%'
    )

def culture() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Culture"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "Do nurses around you work together and support each other?",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_teamwork,
                    on_change=ReportState.set_assign_select_teamwork,
                    required=True
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "Do providers around you work well with nursing staff?",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_providers,
                    on_change=ReportState.set_assign_select_providers,
                    required=True
                ),  
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Do you feel like your input is valued
                    as a part of the care team?""",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_contributions,
                    on_change=ReportState.set_assign_select_contributions,
                    required=True
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Do you feel like you have a positive impact on
                    the care of your patients?""",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_impact,
                    on_change=ReportState.set_assign_select_impact,
                    required=True
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Do you feel like management supports nursing interests?""",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never", "N/A"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_management,
                    on_change=ReportState.set_assign_select_management,
                    required=True
                ),
                width='100%'
            ),
            width='100%'
        ),
        width='100%'
    )

def burnout() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Recommendations"
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "Do you plan on making career changes in the next year or so?"
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_leaving,
                    on_change=ReportState.set_assign_select_leaving,
                    required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.is_leaving,
                rx.vstack(
                    rx.text(
                        "What's your next move?"
                    ),
                    rx.select(
                        [
                            "Same hospital, different job",
                            "Different hospital, same job",
                            "Different hospital, different job",
                            "Advancing nursing career",
                            "Leaving nursing entirely"
                        ],
                        placeholder="- Select -",
                        value=ReportState.assign_select_leaving_reason,
                        on_change=ReportState.set_assign_select_leaving_reason,
                        required=True
                    ),
                    width='100%'
                )
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
                    "(Optional) Any comments for your nursing peers about your experience on the job?",
                    text_align='center'
                ),
                rx.debounce_input(
                    rx.text_area(
                        ReportState.assign_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_assign_input_comments,
                        on_blur=ReportState.set_assign_input_comments,
                        height='10em'
                    ),
                    debounce_timeout=1000
                ),
                rx.cond(
                    ReportState.assign_input_comments,
                    # If there is an entry in the comments
                    rx.cond(
                        ReportState.assign_input_comments_chars_over,
                        # If chars over limit of 500.
                        rx.callout(
                            "Please limit response to < 500 characters!",
                            icon="alert_triangle",
                            color_scheme="red",
                            role="alert"
                        ),
                        # If chars not over limit of 500.
                        rx.text(
                            f"{ReportState.assign_input_comments_chars_left} chars left.",
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
                    "How would you grade your assignment overall?",
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
                    on_click=ReportState.set_assign_select_overall("a")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_b.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_select_overall("b")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_c.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_select_overall("c")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_d.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_select_overall("d")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_f.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_select_overall("f")
                ),
                width='100%'
            ),
            rx.cond(
                ~ReportState.assign_select_overall,
                rx.callout(
                    "Please make a selection.",
                    icon="alert_triangle",
                    color_scheme="red",
                    role="alert"
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.assign_select_overall.upper()} - {ReportState.assign_select_overall_description}",
                        color='white',
                        text_align='center'
                    ),
                    background=ReportState.assign_select_overall_background,
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
        rx.button(
            "Back",
            width='100%',
            on_click=ReportState.report_nav('assignment/summary'),
        ),
        rx.button("Next",
            width='100%',
            type='submit',
        ),
        width='50%',
    )