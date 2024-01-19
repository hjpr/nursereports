
from ..components.footer import footer
from ..components.progress_bar import progress_bar
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import spacer
from ..states.report import ReportState

import reflex as rx

def pay() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        progress_bar(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.center(
                rx.vstack(
                    rx.heading("Pay"),
                    # EMPLOYMENT STATUS
                    # EMPLOYMENT TYPE
                    # PAY
                    # DIFFERENTIAL
                    # CRITICAL STAFFING
                    # BENEFITS
                    # SHIFT
                    # AVERAGE DAYS WORKED A WEEK
                    # ADEQUATELY COMPENSATED
                    # (CONTEXTUAL) DESIRED ADDITIONAL COMPENSATION
                    # TIME AT HOSPITAL AS RN
                    # TOTAL EXPERIENCE AS RN
                    # COMPENSATION GRADE
                    # ADDITIONAL PAY COMMENTS
                    rx.button_group(
                        rx.button("Back",
                                on_click=ReportState.nav_pay_to_summary,
                                is_loading=~rx.State.is_hydrated
                                ),
                        rx.button("Next",
                                on_click=ReportState.nav_pay_to_staffing,
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