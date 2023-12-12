
from ..components.decorators import protected_page
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.custom import dropdown_pair, spacer
from typing import Dict, List, Literal

import reflex as rx

class ReportState(rx.State):

    location: Literal["search", "summary", "unit", "pay", "staffing", "complete"] = "search"
    hospital_id: int
    search_state: str
    search_city: str
    search_results: dict
    
    @rx.cached_var
    def has_search_results(self) -> bool:
        return True if self.search_results else False

class Report(rx.Base):

    route: str = "/report"

    @protected_page
    def page(self) -> rx.Component:
        return rx.box(

            navbar(),

            # SETS TOP OF PAGE FROM UNDERNEATH NAVBAR/C2A    
            c2a_spacer(),

            # MAIN CONTENT CONTAINER
            rx.container(
                rx.cond(
                    ReportState.location == "search",
                    self.search()
                ),
                rx.cond(
                    ReportState.location == "summary",
                    self.summary()
                ),
                rx.cond(
                    ReportState.location == "unit",
                    self.unit()
                ),
                rx.cond(
                    ReportState.location == "pay",
                    self.pay()
                ),
                rx.cond(
                    ReportState.location == "staffing",
                    self.staffing()
                ),
                rx.cond(
                    ReportState.location == "complete",
                    self.complete()
                )

            ),

            footer(),

        )
    
    def search(self) -> rx.Component:
        return rx.center(
            rx.vstack(
                rx.heading("Find your hospital"),
                rx.hstack(
                    rx.select(
                        placeholder="Select state"
                    ),
                    rx.select(
                        placeholder="Select city"
                    )
                ),
                rx.vstack(
                    rx.cond(
                        ReportState.has_search_results,
                        self.get_hospitals_by_location()
                    )
                )
            )
        )

    def summary() -> rx.Component:
        return rx.center(
            rx.vstack(
                rx.heading(
                    "Submit a report."
                ),
                rx.text(
                    """Before you get started, we'd like you to know some important information. 
                    Any details provided to verify your identity, or create a more
                    focused experience, is hidden from users reading your review. This identifying
                    information is also not shared with any third parties. We take your privacy
                    seriously and believe that selling personal data is unethical.
                    
                    The information you provide to us is for the sole benefit of the nursing
                    profession, to support sustainable careers, and to hold institutions
                    accountable for their business practices in ways not previously possible.

                    Our survey is approximately 30 questions and should take around 4-6 minutes.
                    """
                ),
                rx.button(
                    "Got it. Let's go!",
                    on_click=ReportState.set_location("unit"),
                    is_loading=~rx.State.is_hydrated,
                )
            )
        )

    def unit(self) -> rx.Component:
        return rx.center(
            rx.vstack(
                # UNIT OR AREA NAME
                dropdown_pair(
                    "unit_or_area_name",
                    "What's the unit or area you work at?",
                    "Select one.",
                    self.get_unit_or_area_options(),
                ),
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
                            on_click=ReportState.set_location("pay"),
                            is_loading=~rx.State.is_hydrated
                            ),
                    rx.button("Next",
                            on_click=ReportState.set_location("summary"),
                            is_loading=~rx.State.is_hydrated
                            )
                )
            )
        )
    
    def pay() -> rx.Component:
        return rx.center(
            rx.vstack(
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
    
    def get_search_results(form_data) -> Dict:
        pass
    
    def get_hospitals_by_location(form_data) -> rx.Component:
        pass
    
    def get_unit_or_area_options(hospital_id) -> List[str]:
        pass
