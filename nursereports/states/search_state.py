
from ..client.components.lists import cities_by_state, state_abbr_dict
from ..server.supabase.search_requests import supabase_get_hospital_search_results
from ..states import BaseState, ReportState

from typing import Callable, Iterable

import reflex as rx

class SearchState(BaseState):
    search_is_loading: bool

    selected_state: str

    selected_city: str

    last_searched_state: str

    last_searched_city: str

    search_results: list[dict]
    
    error_search: str
        
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

    def event_state_city_selected(self, selection: str) -> None:
        self.selected_city = selection

    def event_state_search(self) -> None:
        """
        Ensure that everything is properly selected, as well as
        prevent user from triggering search button unless a new
        selection is made.
        """
        if (self.selected_state and self.selected_city and not
            (self.selected_state == self.last_searched_state and
             self.selected_city == self.last_searched_city)):
            response = supabase_get_hospital_search_results(
                self.access_token,
                state_abbr_dict[self.selected_state],
                self.selected_city
            )
            if response['success']:
                self.last_searched_state = self.selected_state
                self.last_searched_city = self.selected_city
                search_results = response['payload']
                for hospital in search_results:
                    hospital["hosp_city"] = hospital["hosp_city"].title()
                self.search_results = search_results
            else:
                self.error_search = response['status']

    def clear_search_results(self) -> None:
        self.selected_city = ""
        self.selected_state = ""
        self.search_results = []

    def redirect_to_hospital_overview(self, hosp_id: str) -> Iterable[Callable]:
        return rx.redirect(f"/hospital/{hosp_id}")

    def redirect_to_red_flag_report(self, hosp_id: str) -> Iterable[Callable]:
        return rx.redirect(f"/report/red-flag-report/{hosp_id}/overview")
        
    def redirect_to_full_report(self, hospital_id: str) -> Iterable[Callable]:
        """Do all the things here required for user to access the full report page. User will be
        denied access if variables aren't set correctly."""
        yield ReportState.reset_report
        yield ReportState.set_hospital_id(hospital_id)
        yield ReportState.generate_report_id
        yield ReportState.event_state_get_hospital_info
        yield rx.redirect("/report/full-report/overview")