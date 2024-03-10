
from ..client.components.lists import cities_by_state, state_abbr_dict
from ..server.supabase.search import supabase_get_hospital_search_results
from ..states.base import BaseState

from loguru import logger
from typing import Callable, Iterable, List

import os
import reflex as rx

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")

class SearchState(BaseState):
    selected_state: str
    selected_city: str
    search_results: list[dict]
    error_search: str

    @rx.var
    def url_context(self) -> str:
        return self.router.page.params.get('context')
    
    @rx.var
    def url_for_report(self) -> str:
        if self.url_context == 'report':
            return "/summary"
        else:
            return ""
        
    @rx.cached_var
    def state_options(self) -> list[str]:
        return [state for state in state_abbr_dict.keys()]
    
    @rx.cached_var
    def city_options(self) -> list[str]:
        if self.selected_state:
            state_abbr = state_abbr_dict[self.selected_state]
            return sorted(cities_by_state.get(state_abbr))
        else:
            return []

    def event_state_state_selected(self, selection: str) -> None:
        self.selected_state = selection
        self.selected_city = ""
        self.search_results = []

    def event_state_city_selected(self, selection: str) -> None:
        self.selected_city = selection
        self.search_results = []

    def event_state_search(self) -> None:
        if self.selected_state and self.selected_city:
            state = state_abbr_dict[self.selected_state]
            city = self.selected_city
            response = supabase_get_hospital_search_results(
                self.access_token,
                state,
                city
            )
            if response['success']:
                self.search_results = response['payload']
            else:
                self.error_search = response['status']
        
    def nav_to_report(self, summary_id) -> Callable:
        self.selected_city = ""
        self.selected_state = ""
        self.search_results = []
        return rx.redirect(f"/report/summary/{summary_id}")