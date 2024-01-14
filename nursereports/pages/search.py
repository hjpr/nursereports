
from ..components.cities_by_state import cities_by_state
from ..components.custom import spacer
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from loguru import logger
from reflex.event import Event
from typing import Iterable

import httpx
import json
import os
import reflex as rx
import rich

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

"""
To use this search for reporting, use url /search/report which will
redirect user to /report/hosp_id.

To use this search for finding hospitals, use url /search/hospital
which will redirect user to /hospital/hosp_id.
"""

class SearchState(rx.State):
    selected_state: str
    selected_city: str
    current_search_range: int = 10
    range_options: list[int] = [10, 20, 50]

    @rx.var
    def search_range(self) -> str:
        """
        Returns string used for API call to set range of search
        results returned.
        """
        if self.current_search_range == 10:
            return "0-9"
        if self.current_search_range == 20:
            return "0-20"
        if self.current_search_range == 50:
            return "0-50"

    @rx.var
    def url_context(self) -> str:
        return self.router.page.params.get('context')
        
    @rx.var
    def state_options(self) -> list:
        return [cities for cities in cities_by_state.keys()]
    
    def clear_city_and_state_selection(self) -> Iterable[Event]:
        yield SearchState.set_selected_state("")
        yield SearchState.set_selected_city("")
    
    def clear_city_with_selection(self, selection: str) -> Iterable[Event]:
        yield SearchState.set_selected_state(selection)
        yield SearchState.set_selected_city("")
    
    @rx.var
    def city_options(self) -> list:
        if self.selected_state:
            return sorted(cities_by_state.get(self.selected_state))
        else:
            return []
        
    @rx.cached_var
    def search_results(self) -> list[dict[str, str]]:
        if self.selected_state and self.selected_city:
            access_token = rx.State.get_cookies(self).get("access_token")
            url = f"{api_url}/rest/v1/hospitals"\
            f"?hosp_state=ilike.{self.selected_state}"\
            f"&hosp_city=ilike.{self.selected_city}"\
            "&select=*"
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Range": f"{self.search_range}"
            }
            response = httpx.get(
                url=url,
                headers=headers
            )
            if response.is_success:
                rich.inspect(response)
                logger.debug("Response from Supabase.")
                list_of_hospitals = json.loads(response.content)
                for hospital in list_of_hospitals:
                    hospital['hosp_name'] = hospital['hosp_name'].title()
                return list_of_hospitals
            else:
                rich.inspect(response)
                logger.critical("Getting search results failed!")
        else:
            return []
        

def search() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
         rx.flex(
            # SEARCH SELECT CONTAINER
            rx.vstack(
                rx.heading(
                    "Find your hospital",
                    size='md',
                    ),
                spacer(height='20px'),
                rx.hstack(
                    rx.select(
                        SearchState.state_options,
                        placeholder="Select state",
                        id="selected_state",
                        on_change=SearchState.clear_city_with_selection
                    ),
                    rx.select(
                       SearchState.city_options,
                        placeholder="Select city",
                        value=SearchState.selected_city,
                        id="selected_city",
                        on_change=SearchState.set_selected_city
                    ),
                    width=['100%', '100%', '600px', '600px', '600px'],
                ),
                rx.accordion(
                    rx.accordion_item(
                        rx.accordion_button(
                            rx.text("Filters"),
                            rx.accordion_icon()
                        ),
                        rx.accordion_panel(
                            rx.center(
                                rx.text(
                                    "Results per page",
                                    width='100%'
                                    ),
                                rx.spacer(),
                                rx.select(
                                    SearchState.range_options,
                                    on_change=SearchState.set_current_search_range,
                                )
                            )
                        )
                    ),
                    allow_toggle=True,
                    width='100%'
                ),

                spacer(height='40px'),

                search_results(),

                spacer(height='40px'),

                # STYLING FOR SEARCH SELECT CONTAINER
                width=['100%', '100%', '600px', '600px', '600px'],
            ),

            # STYLING FOR MAIN CONTENT CONTAINER
            padding_x='10px',
            width='100%',
            max_width='1200px',
            align='center',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
        ),

        footer(),

        # STYLING FOR PAGE BODY
        width='100%',
        flex_direction='column',
        align='center',
        min_height='100vh',
    )

def search_results() -> rx.Component:
    return rx.cond(
        SearchState.search_results,
        rx.foreach(
            SearchState.search_results,
            render_results
        )
    )

def render_results(result: dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text(f"{result['hosp_name']}"),
            rx.spacer(),
            rx.link(
                "Select",
                color_scheme='teal',
                href=f"/{SearchState.url_context}/{result['hosp_id']}",
                on_click=SearchState.clear_city_and_state_selection
            ),
            flex_direction='row'
        ),
        width='100%',
    )
