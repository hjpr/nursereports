from ..components.custom import spacer
from ..components.footer import footer
from ..components.lists import unit_specialties
from ..components.navbar import navbar, c2a_spacer
from ..components.report_progress import progress
from ..states.report import ReportState

import reflex as rx

def assign_page() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.form(
                rx.vstack(

                    spacer(height='10px'),

                    progress(),

                    spacer(height='10px'),

                    description(),

                    unit(),

                    specialty(),

                    culture(),

                    burnout(),

                    comments(),    

                    overall(),

                    spacer(height='40px'),

                    buttons(),

                    spacer(height='40px'),

                    spacing='1em'
                ),
                on_submit=ReportState.handle_submit_unit
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
                    "Assignment",
                    size='lg'
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
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def unit() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Info",
                    size='md'
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
                    value=ReportState.assign_specific_unit,
                    variant='filled',
                    on_change=ReportState.set_assign_specific_unit,
                    is_required=True
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
                            variant='filled',
                            on_change=ReportState.set_assign_select_unit,
                            is_required=True
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
                                        is_required=True
                                    ),
                                    debounce_timeout=1000
                                ),
                                rx.cond(
                                    ReportState.name_too_long,
                                    rx.alert(
                                        rx.alert_icon(),
                                        rx.alert_title(
                                            "Invalid unit name. Too long!"
                                        ),
                                        status='warning'
                                    )
                                ),
                                width='100%'
                            ),
                            spacing='2em',
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
                            variant='filled',
                            on_change=ReportState.set_assign_select_acuity,
                            is_required=True
                        ),
                        width='100%'
                    ),
                    spacing='2em',
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
                            variant='filled',
                            on_change=ReportState.set_assign_select_area,
                            is_required=True
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
                    spacing='2em',
                    width='100%'
                )
            ),
            spacing='2em',
            width='100%'
        ),
        width="100%"
    )

def specialty() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Specialty",
                    size='md'
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
                        variant='filled',
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
                            variant='filled',
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
                            variant='filled',
                            on_change=ReportState.set_assign_select_specialty_3,
                        ),
                        width='100%' 
                    )
                ),
                spacing='2em',
                width='100%'
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def culture() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Culture",
                    size='md'
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.box(
                    rx.span("Do "),
                    rx.span(
                        "nurses ",
                        font_weight='bold'
                    ),
                    rx.span("in your unit or area work together and support each other?"),
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_teamwork,
                    variant='filled',
                    on_change=ReportState.set_assign_select_teamwork,
                    is_required=True
                ),
                width='100%'
            ),
            rx.vstack(
                rx.box(
                    rx.span("Do "),
                    rx.span(
                        "providers ",
                        font_weight='bold'
                    ),
                    rx.span("in your unit or area work well with nursing staff?"),
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_providers,
                    variant='filled',
                    on_change=ReportState.set_assign_select_providers,
                    is_required=True
                ),  
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Do you feel like your contributions are valued
                    as a part of the care team?""",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_contributions,
                    variant='filled',
                    on_change=ReportState.set_assign_select_contributions,
                    is_required=True
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
                    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_impact,
                    variant='filled',
                    on_change=ReportState.set_assign_select_impact,
                    is_required=True
                ),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Do you feel like management supports you?""",
                    text_align='center'
                ),
                rx.select(
                    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
                    placeholder="- Select -",
                    value=ReportState.assign_select_tools,
                    variant='filled',
                    on_change=ReportState.set_assign_select_tools,
                    is_required=True
                ),
                width='100%'
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def burnout() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Recommendations",
                    size='md'
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
                    variant='filled',
                    on_change=ReportState.set_assign_select_leaving,
                    is_required=True
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
                        variant='filled',
                        on_change=ReportState.set_assign_select_leaving_reason,
                        is_required=True
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
                    variant='filled',
                    on_change=ReportState.set_assign_select_recommend,
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
                        """Any comments for your nursing peers about culture, management,
                        or other experiences relevant to nursing at your assignment?""",
                        text_align='center'
                    ),
                    rx.debounce_input(
                        rx.text_area(
                            ReportState.assign_input_comments,
                            placeholder="(Optional) Do not enter personally identifiable information.",
                            on_change=ReportState.set_assign_input_comments,
                            on_blur=ReportState.set_assign_input_comments,
                            variant='filled',
                            height='10em'
                        ),
                        debounce_timeout=1000
                    ),
                    width='100%'
                ),
                rx.cond(
                    ReportState.assign_input_comments,
                    # If there is an entry in the comments
                    rx.cond(
                        ReportState.assign_input_comments_chars_over,
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
                            f"{ReportState.assign_input_comments_chars_left} chars left.",
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
                    on_click=ReportState.set_assign_overall("a")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_b.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_overall("b")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_c.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_overall("c")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_d.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_overall("d")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_f.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_assign_overall("f")
                ),
                width='100%'
            ),
            rx.cond(
                ~ReportState.assign_overall,
                rx.alert(
                    rx.alert_icon(),
                    rx.alert_title(
                        "Please make a selection."
                    ),
                    border_radius='5px',
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.assign_overall.upper()} - {ReportState.assign_overall_description}",
                        color='white',
                        text_align='center',
                        size='lg'
                    ),
                    background=ReportState.assign_overall_background,
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
    return rx.center(
        rx.button_group(
            rx.button("Back",
                    width='100%',
                    on_click=ReportState.report_nav('staffing'),
                    is_loading=~rx.State.is_hydrated,
                    color_scheme='teal'
            ),
            rx.button("Submit",
                    width='100%',
                    type_='submit',
                    is_loading=~rx.State.is_hydrated,
                    is_disabled=~ReportState.assign_can_progress,
                    color_scheme='teal'
            ),
            width='50%',
        ),
        width='100%'
    )