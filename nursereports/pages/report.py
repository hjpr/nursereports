
from ..components.decorators import protected_page
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..components.cities_by_state import cities_by_state
from ..components.custom import spacer
from typing import Dict, List, Literal

import httpx
import reflex as rx
import os
import rich

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

class ReportState(rx.State):

    location: Literal["search", "summary", "unit", "pay", "staffing", "complete"] = "search"
    hospital_id: int
    selected_state: str
    selected_city: str

    # Answer Vars
    unit_or_area_name: str

    @rx.cached_var
    def city_options(self) -> list:
        if bool(self.is_state_selected):
            return cities_by_state.get(ReportState.selected_state)
        else:
            return []

    @rx.cached_var
    def is_state_selected(self) -> bool:
        return bool(self.selected_state)
    
    @rx.cached_var
    def has_search_results(self) -> bool:
        return bool(self.search_results)
    
    @rx.cached_var
    def search_results(self) -> Dict:
        if bool(self.selected_state) and bool(self.selected_city):
            return get_search_results(self.selected_state, self.selected_city)
        

@protected_page
def report() -> rx.Component:
    return rx.box(

        navbar(),

        # SETS TOP OF PAGE FROM UNDERNEATH NAVBAR/C2A    
        c2a_spacer(),

        # MAIN CONTENT CONTAINER
        rx.container(
            rx.cond(
                ReportState.location == "search",
                search()
            ),
            rx.cond(
                ReportState.location == "summary",
                summary()
            ),
            rx.cond(
                ReportState.location == "unit",
                unit()
            ),
            rx.cond(
                ReportState.location == "pay",
                pay()
            ),
            rx.cond(
                ReportState.location == "staffing",
                staffing()
            ),
            rx.cond(
                ReportState.location == "complete",
                complete()
            )

        ),

        footer(),

    )

def search() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Find your hospital"),
            rx.hstack(
                rx.select(
                    [key for key in cities_by_state.keys()],
                    placeholder="Select state",
                    is_required=True,
                    on_change=ReportState.set_selected_state
                ),
                rx.cond(
                    ReportState.is_state_selected,
                    rx.select(
                        ReportState.city_options,
                        placeholder="Select city",
                        is_required=True,
                        on_change=ReportState.set_selected_city
                    )
                )
            ),
            rx.vstack(
                rx.cond(
                    ReportState.has_search_results,
                    get_hospitals_by_location()
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

def unit() -> rx.Component:
    return rx.center(
        rx.vstack(
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

async def get_search_results(state, city) -> Dict:
    async with httpx.AsyncClient() as client:
        url = f'{api_url}/rest/v1/hospitals?state=ilike.{state}&city=ilike.{city}'
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}"
        }
        response = await client.get(
            url=url,
            headers=headers
        )
        if response.is_success:
            rich.inspect(response)
        else:
            print("Getting search results failed!")

def get_hospitals_by_location() -> rx.Component:
    return rx.box(
        rx.text("Search successful")
    )
