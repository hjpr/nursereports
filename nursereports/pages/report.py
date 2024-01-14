
from loguru import logger

from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.cities_by_state import cities_by_state
from ..components.custom import spacer

import reflex as rx
import os

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

class ReportState(rx.State):
    location: str = "summary"
    unit_or_area_name: str = None

    @rx.var
    def hosp_id(self) -> str:
        return self.router.page.params.get('hosp_id')
                

def report() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.cond(
                ReportState.location == 'summary',
                summary()
            ),
            rx.cond(
                ReportState.location == 'unit',
                unit()
            ),
            rx.cond(
                ReportState.location == 'pay',
                pay()
            ),
            rx.cond(
                ReportState.location == 'staffing',
                staffing()
            ),
            rx.cond(
                ReportState.location == 'complete',
                complete()
            ),

            # STYLING FOR CONTENT CONTAINER
            padding='0 0 0 0',
            width='100%',
            max_width='1200px',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',

        ),

        spacer(height='40px'),

        footer(),

        # STYLING FOR BODY CONTAINER
        width='100%',
        flex_direction='column',

        align_items='center',
        min_height='100vh',
    )

def summary() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Submit a report."
            ),
            rx.text(
                """Before you get started, read this. 
                Any personal details given to us throughout the report process is hidden
                from users reading your review. This identifying
                information is also not shared with any third parties. We take your privacy
                seriously and believe that selling personal data is unethical.
                The information you provide to us is for the sole benefit of the nursing
                community. Our survey is 30-ish questions and should take about 4-6 minutes.
                """
            ),
            rx.button(
                "Got it. Let's go!",
                on_click=ReportState.set_location("unit"),
                is_loading=~rx.State.is_hydrated,
            )
        )
    )

def unit() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Unit"),
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
                        on_click=ReportState.set_location("summary"),
                        is_loading=~rx.State.is_hydrated
                        ),
                rx.button("Next",
                        on_click=ReportState.set_location("pay"),
                        is_loading=~rx.State.is_hydrated
                        )
            )
        )
    )

def pay() -> rx.Component:
    return rx.center(
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
                        on_click=ReportState.set_location("unit"),
                        is_loading=~rx.State.is_hydrated
                        ),
                rx.button("Next",
                        on_click=ReportState.set_location("staffing"),
                        is_loading=~rx.State.is_hydrated
                        )
            )
        ),
    )

def staffing() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Staffing"),
            # STAFFING RATIOS
            # STAFFING SAFETY
            # WORKLOAD RATING
            # WORKLOAD SAFETY
            # ADEQUATE SUPPORT STAFF
            # ADEQUATE RESOURCES
            # BURNOUT
            # DESIRE TO STAY/LEAVE
            # STAFFING GRADE
            # ADDITIONAL STAFFING COMMENTS
            rx.button_group(
                rx.button("Back",
                        on_click=ReportState.set_location("pay"),
                        is_loading=~rx.State.is_hydrated
                        ),
                rx.button("Next",
                        on_click=ReportState.set_location("complete"),
                        is_loading=~rx.State.is_hydrated
                )
            )
        )
    )

def complete() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Wow, what a healthcare hero!"),
            rx.text(
                """We'd throw you a pizza party, but that's a real logistical
                nightmare, so instead check out our database of high quality
                reports to learn about the current landscape of nursing jobs."""
            ),
            rx.button(
                "Let's get started!",
                on_click=rx.redirect('/dashboard'),
                is_loading=~rx.State.is_hydrated
            )
        )
    )
