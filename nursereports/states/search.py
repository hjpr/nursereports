
from ..client.components.lists import cities_by_state, state_abbr_dict
from ..states.base import BaseState

from loguru import logger
from typing import Callable, Iterable

import httpx
import json
import os
import reflex as rx

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

class SearchState(BaseState):
    selected_state: str
    selected_city: str
    current_search_range: int = "10"
    range_options: list[str] = ["10", "20", "50"]

    @rx.var
    def search_range(self) -> str:
        if self.current_search_range == "10":
            return "0-9"
        if self.current_search_range == "20":
            return "0-20"
        if self.current_search_range == "50":
            return "0-50"

    @rx.var
    def url_context(self) -> str:
        """
        To use this search for reporting, use url /search/report which will
        redirect user to /report/id/{hosp_id}.

        To use this search for finding hospitals, use url /search/hospital
        which will redirect user to /hospital/id/{hosp_id}.
        """
        return self.router.page.params.get('context')
    
    @rx.var
    def url_for_report(self) -> str:
        if self.url_context == 'report':
            return "/summary"
        else:
            return ""
        
    @rx.var
    def state_options(self) -> list[str]:
        return [state for state in state_abbr_dict.keys()]

    def do_selected_state(self, selection: str) -> Iterable[Callable]:
        self.selected_state = selection
        self.selected_city = ""

    def do_selected_city(self, selection: str) -> Iterable[Callable]:
        self.selected_city = selection

    @rx.var
    def city_options(self) -> list[str]:
        if self.selected_state:
            state_to_abbr = state_abbr_dict[self.selected_state]
            return sorted(cities_by_state.get(state_to_abbr))
        else:
            return []
        
    @rx.var
    def results_failed(self) -> bool:
        if self.search_results:
            if self.search_results[0] == "Unauthorized":
                return True
            else:
                False
        else:
            False
        
    @rx.cached_var
    def search_results(self) -> list[dict[str, str]]:
        if self.selected_state and self.selected_city and self.url_context:
            state_to_abbr = state_abbr_dict[self.selected_state]
            url = f"{api_url}/rest/v1/hospitals"\
            f"?hosp_state=ilike.{state_to_abbr}"\
            f"&hosp_city=ilike.{self.selected_city}"\
            "&select=*"
            headers = {
                "apikey": api_key,
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Range": f"{self.search_range}"
            }

            response = httpx.get(
                url=url,
                headers=headers
            )
            
            if response.is_success:
                logger.debug("Response from Supabase.")
                list_of_hospitals = json.loads(response.content)
                for hospital in list_of_hospitals:
                    hospital['hosp_name'] = hospital['hosp_name'].title()
                    hospital['hosp_addr'] = hospital['hosp_addr'].title()
                return list_of_hospitals
            else:
                if response.status_code == 401:
                    return [response.reason_phrase]
        else:
            return []
        
    def nav_to_report(self, summary_id) -> Iterable[Callable]:
        self.selected_city = ""
        self.selected_state = ""
        yield rx.redirect(f"/report/summary/{summary_id}")