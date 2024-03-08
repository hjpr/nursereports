
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.lists import years_experience
from ..components.navbar import navbar
from ..components.report_progress import progress
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx


@rx.page(
        route="/report/submit/[report_id]/compensation",
        title="Nurse Reports",
        on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def comp_page() -> rx.Component:
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
                    pay(),
                    demographics(),
                    benefits(),
                    compensation(),
                    overall(),
                    comments(),
                    spacer(height='40px'),
                    buttons(),
                    spacer(height='40px'),
                ),
                on_submit=ReportState.handle_submit_comp,
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
                    "Compensation"
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
            width='100%'
        )
    )

def pay() -> rx.Component:
    return rx.card(
        rx.vstack(
            # PAY - EMPLOYMENT TYPE ---------------------------------
            rx.vstack(
                rx.heading(
                    "Pay"
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
                    on_change=ReportState.set_comp_select_emp_type,
                    required=True
                ),
                width='100%'
            ),
            # PAY - PAY TYPE ----------------------------------------
            rx.vstack(
                rx.text(
                    "Are you paid at an hourly or weekly rate?"
                ),
                rx.select(
                    ["Hourly", "Weekly"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_pay_type,
                    on_change=ReportState.set_comp_select_pay_type,
                    required=True
                ),
                width='100%'
            ),
            # PAY - PAY AMOUNT --------------------------------------
            rx.cond(
                ReportState.comp_select_pay_type,
                rx.cond(
                    ReportState.is_weekly,
                    # If weekly
                    rx.vstack(
                        rx.text(
                            "Total rate per week? (in $)",
                            text_align='center'
                        ),
                        rx.chakra.number_input(
                            value=ReportState.comp_input_pay_amount,
                            input_mode='numeric',
                            on_change=ReportState.set_comp_input_pay_amount,
                            is_required=True,
                        ),
                        rx.cond(
                            ReportState.is_pay_invalid,
                            rx.callout(
                                "A valid weekly rate must be entered.",
                                icon='info'
                            )
                        ),
                        width='100%'
                    ),
                    # If hourly
                    rx.vstack(
                        rx.text(
                            " Base rate per hour? (in $)",
                            text_align='center'
                        ),
                        rx.chakra.number_input(
                            value=ReportState.comp_input_pay_amount,
                            input_mode='numeric',
                            on_change=ReportState.set_comp_input_pay_amount,
                            is_required=True,
                        ),
                        rx.cond(
                            ReportState.is_pay_invalid,
                            rx.callout(
                                "A valid hourly rate must be entered.",
                                icon='info'
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
                    on_change=ReportState.set_comp_select_diff_response,
                    required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.gets_differential,
                rx.vstack(
                    rx.vstack(
                        rx.text("(Optional) Extra per hour for nights? (in $)"),
                        rx.chakra.number_input(
                            value=ReportState.comp_input_diff_nights,
                            on_change=ReportState.set_comp_input_diff_nights,
                            max=50
                        )
                    ),
                    rx.vstack(
                        rx.text("(Optional) Extra per hour for weekends? (in $)"),
                        rx.chakra.number_input(
                            value=ReportState.comp_input_diff_weekends,
                            on_change=ReportState.set_comp_input_diff_weekends,
                            max=50
                        )
                    ),
                    width='100%'
                )
            ),
            # PAY - INCENTIVE BONUS ---------------------------------
            rx.vstack(
                rx.text(
                    """Does your hospital have special incentive pay for
                    certain shifts? (e.g. critical shift pay)""",
                    text_align='center'
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_incentive_response,
                    on_change=ReportState.set_comp_select_incentive_response,
                    required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.gets_incentive,
                rx.vstack(
                    rx.text(
                        "(Optional) Extra per hour for incentive? (in $)"
                    ),
                    rx.chakra.number_input(
                        value=ReportState.comp_input_incentive_amount,
                        on_change=ReportState.set_comp_input_incentive_amount,
                        max_=100
                    )
                )
            ),
            rx.vstack(
                rx.text(
                    """Does your hospital pay extra for having certifications?
                    (e.g. CCRN, CWON, RN-BC)""",
                    text_align='center'
                    ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_certifications,
                    on_change=ReportState.set_comp_select_certifications,
                    required=True
                ),
                width='100%'
            ),
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
                    on_change=ReportState.set_comp_select_shift,
                    required=True
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
                    required=True
                ),
                width='100%'
            ),
            # DEMO - TIME AT HOSPITAL AS RN -------------------------
            rx.vstack(
                rx.text(
                    "How many years have you worked at this hospital as a RN?"
                ),
                rx.select(
                    years_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_hospital_experience,
                    on_change=ReportState.set_comp_select_hospital_experience,
                    required=True
                ),
                width='100%'
            ),
            # DEMO - TOTAL EXPERIENCE AS RN -------------------------
            rx.vstack(
                rx.text(
                    "How many years in total have you worked as a RN?"
                ),
                rx.select(
                    years_experience,
                    placeholder="- Select -",
                    value=ReportState.comp_select_total_experience,
                    on_change=ReportState.set_comp_select_total_experience,
                    required=True
                ),
                width='100%'
            ),
            rx.cond(
                ReportState.is_experience_invalid,
                rx.callout(
                    "Can't have less total years than years at current hospital.",
                    icon="alert_triangle",
                    color_scheme="red",
                    role='alert'
                )
            ),
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
                        checked=ReportState.comp_check_benefit_pto
                    ),
                    rx.text("PTO"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_parental,
                        checked=ReportState.comp_check_benefit_parental
                        ),
                    rx.text("Parental Leave"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_insurance,
                        checked=ReportState.comp_check_benefit_insurance
                        ),
                    rx.text("Insurance"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_retirement,
                        checked=ReportState.comp_check_benefit_retirement
                        ),
                    rx.text("Retirement"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_tuition,
                        checked=ReportState.comp_check_benefit_tuition
                        ),
                    rx.text("Tuition Aid"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                rx.hstack(
                    rx.checkbox(
                        on_change=ReportState.set_comp_check_benefit_pro_dev,
                        checked=ReportState.comp_check_benefit_pro_dev
                        ),
                    rx.text("Professional Development"),
                    padding_x='0.5em',
                    padding_y='1em'
                ),
                width='100%',
                wrap='wrap',
                justify='center'
            ),
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
                ),
                rx.divider(),
                width='100%'
            ),
            # COMP - ADEQUATELY COMPENSATED -------------------------
            rx.vstack(
                rx.text(
                    """Is your overall pay and benefits package generally
                    enough to keep you satisfied in your current role?""",
                    text_align='center'
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select -",
                    value=ReportState.comp_select_comp_adequate,
                    on_change=ReportState.set_comp_select_comp_adequate,
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
                    "Comments",
                ),
                rx.divider(),
                width='100%'
            ),
            # COMP - COMMENTS ---------------------------------------
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
                        rx.callout(
                            "Please limit response to < 500 characters!",
                            icon="alert_triangle",
                            color_scheme="red",
                            role="alert"
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
            width='100%'
        ),
        width='100%'
    )

def overall() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    "Grade"
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
                rx.callout(
                    "Please make a selection.",
                    icon="info"
                ),
                rx.center(
                    rx.heading(
                        f"You graded: {ReportState.comp_select_overall.upper()} - {ReportState.comp_overall_description}",
                        color='white',
                        text_align='center',
                    ),
                    background=ReportState.comp_overall_background,
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
                on_click=ReportState.report_nav('compensation/summary'),
        ),
        rx.button("Next",
                width='100%',
                type='submit',
        ),
        width='50%',
    )