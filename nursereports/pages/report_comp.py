from ..components.custom import spacer
from ..components.footer import footer
from ..components.lists import years_experience
from ..components.navbar import navbar, c2a_spacer
from ..components.report_progress import progress
from ..states.report import ReportState

import reflex as rx

def comp_page() -> rx.Component:
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

                    pay(),

                    demographics(),

                    benefits(),

                    compensation(),

                    overall(),

                    comments(),
                    
                    spacer(height='40px'),

                    buttons(),

                    spacer(height='40px'),

                    spacing='1em'
                ),
                # STYLING FOR FORM
                on_submit=ReportState.handle_submit_comp,
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
                    "Compensation",
                    size='lg'
                ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    """Answer questions about what you recieve as
                    pay and benefits based on your experience, and 
                    if the compensation packages available are
                    acceptable for your position.""",
                ),
            ),
            spacing='2em',
            width='100%'
        )
    )

def pay() -> rx.Component:
    return rx.card(
        rx.vstack(
            # PAY - EMPLOYMENT TYPE ---------------------------------
            rx.vstack(
                rx.heading("Pay",
                        size='md'
                        ),
                rx.divider(),
                width='100%'
            ),
            rx.vstack(
                rx.text(
                    "What is your employment type?"
                    ),
                rx.select(
                    ["Full-time", "Part-time", "Contract"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_emp_type,
                    variant='filled',
                    on_change=ReportState.set_comp_select_emp_type,
                    is_required=True
                ),
                width='100%'
            ),
            # PAY - PAY AMOUNT --------------------------------------
            rx.cond(
                ReportState.comp_select_emp_type,
                rx.cond(
                    ReportState.is_contract,
                    # If contract
                    rx.vstack(
                        rx.box(
                            rx.span("Total rate "),
                            rx.span("per week? ", font_weight='bold'),
                            rx.span("(in $)"),
                            text_align='center'
                        ),
                        rx.number_input(
                            value=ReportState.comp_input_pay_amount,
                            variant='filled',
                            input_mode='numeric',
                            on_change=ReportState.set_comp_input_pay_amount,
                            is_required=True,
                            min_=0
                        ),
                        rx.cond(
                            ReportState.is_pay_invalid,
                            rx.cond(
                                ReportState.is_contract,
                                rx.alert(
                                    rx.alert_icon(),
                                    rx.alert_title(
                                        "A valid weekly rate must be entered."
                                    ),
                                    status='info',
                                    border_radius='5px'
                                )
                            )
                        ),
                        width='100%'
                    ),
                    # If not contract
                    rx.vstack(
                        rx.box(
                            rx.span("Base rate "),
                            rx.span("per hour? ", font_weight='bold'),
                            rx.span("(in $)"),
                            text_align='center'
                        ),
                        rx.number_input(
                            value=ReportState.comp_input_pay_amount,
                            variant='filled',
                            input_mode='numeric',
                            on_change=ReportState.set_comp_input_pay_amount,
                            is_required=True,
                            min_=0

                        ),
                        rx.cond(
                            ReportState.is_pay_invalid,
                            rx.cond(
                                ~ReportState.is_contract,
                                rx.alert(
                                    rx.alert_icon(),
                                    rx.alert_title(
                                        "A valid hourly rate must be entered."
                                    ),
                                    status='info',
                                    border_radius='5px'
                                )
                            )
                        ),
                        width='100%'
                    )
                )
            ),
            # PAY - DIFFERENTIAL ------------------------------------
            rx.vstack(
                rx.text("Do you get extra pay for nights or weekends?"),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_diff_response,
                    variant='filled',
                    on_change=ReportState.set_comp_select_diff_response,
                    is_required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.gets_differential,
                rx.vstack(
                    rx.vstack(
                        rx.text("(Optional) Extra per hour for nights? (in $)"),
                        rx.number_input(
                            value=ReportState.comp_select_diff_nights,
                            variant='filled',
                            on_change=ReportState.set_comp_select_diff_nights,
                        )
                    ),
                    rx.vstack(
                        rx.text("(Optional) Extra per hour for weekends? (in $)"),
                        rx.number_input(
                            value=ReportState.comp_select_diff_weekends,
                            variant='filled',
                            on_change=ReportState.set_comp_select_diff_weekends,
                        )
                    ),
                    spacing='2em',
                    width='100%'
                )
            ),
            # PAY - INCENTIVE BONUS ---------------------------------
            rx.vstack(
                rx.text(
                    """Do you get incentives for picking up extra shifts?
                    (e.g. critical shift pay)""",
                    text_align='center'
                    ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_incentive_response,
                    variant='filled',
                    on_change=ReportState.set_comp_select_incentive_response,
                    is_required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.gets_incentive,
                rx.vstack(
                    rx.text(
                        "(Optional) Extra per hour for incentive? (in $)"
                    ),
                    rx.number_input(
                        value=ReportState.comp_input_incentive_amount,
                        variant='filled',
                        on_change=ReportState.set_comp_input_incentive_amount
                    )
                )
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%',
    )

def demographics() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Demographics",
                    size='md'
                    ),
                rx.divider(),
                width='100%'
            ),
            # DEMO - SHIFTS -----------------------------------------
            rx.vstack(
                rx.text("What shifts do you typically work?"),
                rx.select(
                    ["Day", "Night", "Rotating"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_shift,
                    variant='filled',
                    on_change=ReportState.set_comp_select_shift,
                    is_required=True
                ),
                width='100%'
            ),
            # DEMO - AVERAGE DAYS WORKED A WEEK ---------------------
            rx.vstack(
                rx.text("On average, how many shifts do you work per week?"),
                rx.select(
                    ["1", "2", "3", "4", "5", "6", "7"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_weekly_shifts,
                    on_change=ReportState.set_comp_select_weekly_shifts,
                    variant='filled',
                    is_required=True
                ),
                width='100%'
            ),
            # DEMO - TIME AT HOSPITAL AS RN -------------------------
            rx.vstack(
                rx.box(
                    rx.span("How many "),
                    rx.span(
                        "years at this hospital ",
                        font_weight='bold'
                    ),
                    rx.span("have you worked as a RN?"),
                    text_align='center'
                ),
                rx.select(
                    years_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_hospital_experience,
                    on_change=ReportState.set_comp_select_hospital_experience,
                    variant='filled',
                    is_required=True
                ),
                width='100%'
            ),
            # DEMO - TOTAL EXPERIENCE AS RN -------------------------
            rx.vstack(
                rx.box(
                    rx.span("How many "),
                    rx.span(
                        "years in total ",
                        font_weight='bold'
                    ),
                    rx.span("have you worked as a RN?"),
                    text_align='center'
                ),
                rx.select(
                    years_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_total_experience,
                    on_change=ReportState.set_comp_select_total_experience,
                    variant='filled',
                    is_invalid=ReportState.is_experience_invalid,
                    is_required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.is_experience_invalid,
                rx.alert(
                    rx.alert_icon(),
                    rx.alert_title(
                        "Can't have less total years than years at current hospital."
                    ),
                    status='info',
                    border_radius='5px'
                )
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def benefits() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Benefits",
                    size='md'
                    ),
                rx.text(
                    "Select the benefits that are offered for your position.",
                    text_align='center'
                    ),
                rx.divider(),
                width='100%'
            ),
            rx.hstack(
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_pto,
                        is_checked=ReportState.comp_check_benefit_pto
                        ),
                    rx.text("PTO"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_parental,
                        is_checked=ReportState.comp_check_benefit_parental
                        ),
                    rx.text("Parental Leave"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_insurance,
                        is_checked=ReportState.comp_check_benefit_insurance
                        ),
                    rx.text("Insurance"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_retirement,
                        is_checked=ReportState.comp_check_benefit_retirement
                        ),
                    rx.text("Retirement"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_tuition,
                        is_checked=ReportState.comp_check_benefit_tuition
                        ),
                    rx.text("Tuition Aid"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_pro_dev,
                        is_checked=ReportState.comp_check_benefit_pro_dev
                        ),
                    rx.text("Professional Development"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                width='100%',
                wrap='wrap',
                justify='center'
            ),
            spacing='2em',
            width='100%'
        ),
        width='100%'
    )

def compensation() -> rx. Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Compensation",
                    size='md'
                    ),
                rx.divider(),
                width='100%'
            ),
            # COMP - ADEQUATELY COMPENSATED -------------------------
            rx.vstack(
                rx.text(
                    """Is your compensation generally enough to keep you
                    at this assignment?""",
                    text_align='center'
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_comp_adequate,
                    variant='filled',
                    on_change=ReportState.set_comp_select_comp_adequate,
                    is_required=True
                ),
                width='100%'
            ),
            # COMP - DESIRED ADDITIONAL COMPENSATION ----------------
            rx.cond(
                ReportState.compensation_is_inadequate,
                rx.vstack(
                    rx.text(
                        """(Optional) How could compensation change to make this
                        assignment worthwhile?""",
                        text_align='center'
                    ),
                    rx.debounce_input(
                        rx.text_area(
                            value=ReportState.comp_input_desired_changes,
                            placeholder="Do not enter personally identifiable information.",
                            on_change=ReportState.set_comp_input_desired_changes,
                            on_blur=ReportState.set_comp_input_desired_changes,
                            is_invalid=ReportState.comp_desired_changes_chars_over,
                            height='10em'
                        ),
                        debounce_timeout=1000
                    ),
                    rx.cond(
                        ReportState.comp_input_desired_changes,
                        # If there is an entry in the comments
                        rx.cond(
                            ReportState.comp_desired_changes_chars_over,
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
                                f"{ReportState.comp_desired_changes_chars_left} chars left.",
                                text_align="center"
                            )
                        ),
                        # If no entry yet in comments
                        rx.text(
                            "500 character limit."
                        )
                    )
                )
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
            # COMP - COMMENTS ---------------------------------------
            rx.vstack(
                rx.box(
                    rx.span(
                        "(Optional) Any comments for your nursing peers about"
                    ),
                    rx.span(
                        " pay or benefits?",
                        font_weight='bold'
                    ),
                    text_align='center'
                ),
                rx.debounce_input(
                    rx.text_area(
                        ReportState.comp_input_comments,
                        placeholder="Do not enter personally identifiable information.",
                        on_change=ReportState.set_comp_input_comments,
                        on_blur=ReportState.set_comp_input_comments,
                        is_invalid=ReportState.comp_comments_chars_over,
                        height='10em'
                    ),
                    debounce_timeout=1000
                ),
                rx.cond(
                    ReportState.comp_input_comments,
                    # If there is an entry in the comments
                    rx.cond(
                        ReportState.comp_comments_chars_over,
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
                            f"{ReportState.comp_comments_chars_left} chars left.",
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
            spacing='2em',
            width='100%'
        ),
        width='100%'
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
                    "How would you grade your compensation overall?",
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
                    on_click=ReportState.set_comp_select_overall("a")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_b.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_comp_select_overall("b")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_c.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_comp_select_overall("c")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_d.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_comp_select_overall("d")
                ),
                rx.spacer(),
                rx.image(
                    src='/raster/icons/icon_rating_f.webp',
                    height=['50px', '65px', '75px', '75px', '75px',],
                    width=['50px', '65px', '75px', '75px', '75px',],
                    border_radius='5px',
                    on_click=ReportState.set_comp_select_overall("f")
                ),
                width='100%'
            ),
            rx.cond(
                ~ReportState.comp_select_overall,
                rx.alert(
                    rx.alert_icon(),
                    rx.alert_title(
                        "Please make a selection."
                    ),
                    border_radius='5px',
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.comp_select_overall.upper()} - {ReportState.comp_overall_description}",
                        color='white',
                        text_align='center',
                        size='lg'
                    ),
                    background=ReportState.comp_overall_background,
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
                    on_click=ReportState.report_nav('summary'),
                    is_loading=~rx.State.is_hydrated,
                    color_scheme='teal'
            ),
            rx.button("Next",
                    width='100%',
                    type_='submit',
                    is_loading=~rx.State.is_hydrated,
                    is_disabled=~ReportState.comp_can_progress,
                    color_scheme='teal'
            ),
            width='50%',
        ),
        width='100%'
    )