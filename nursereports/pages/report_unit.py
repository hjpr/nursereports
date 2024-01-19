from ..components.footer import footer
from ..components.progress_bar import progress_bar
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer
from ..states.report import ReportState

import reflex as rx

def unit() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        progress_bar(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.center(
                rx.vstack(
                    rx.heading(
                        "Unit",
                        size='md'
                        ),
                    # UNIT OR AREA NAME
                    # (CONTEXTUAL) UNIT NAME
                    # (CONTEXTUAL) UNIT ABBREVIATION
                    # (CONTEXTUAL) ROLE / AREA
                    # UNIT SPECIALTY
                    # (CONTEXTUAL) UNIT SPECIALTY 2
                    # (CONTEXTUAL) UNIT SPECIALTY 3
                    # ACUITY
                    # NURSING CULTURE
                    # PROVIDER CULTURE
                    # NURSING AUTONOMY
                    # DIRECT MANAGEMENT
                    # SCHEDULE SATISFACTION
                    # WORKPLACE SAFETY
                    # UNIT GRADE
                    # ADDITIONAL UNIT COMMENTS
                    rx.button_group(
                        rx.button("Back",
                                on_click=ReportState.nav_unit_to_staffing,
                                is_loading=~rx.State.is_hydrated
                                ),
                        rx.button("Submit",
                                on_click=ReportState.submit_report,
                                is_loading=~rx.State.is_hydrated
                                )
                    )
                )
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

        spacer(height='80px'),

        footer(),

        # STYLING FOR BODY CONTAINER
        width='100%',
        flex_direction='column',

        align_items='center',
        min_height='100vh',
    )