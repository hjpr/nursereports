from ..client.components.dicts import cities_by_state, state_to_abbr_dict
from ..server.supabase.search_requests import supabase_get_hospital_search_results
from ..states import AuthState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class SearchState(AuthState):
    last_searched_state: str
    last_searched_city: str
    search_is_loading: bool = False
    search_results: list[dict]
    selected_state: str
    selected_city: str

    @rx.var(cache=True)
    def state_options(self) -> list[str]:
        return [state for state in state_to_abbr_dict.keys()]

    @rx.var(cache=True)
    def city_options(self) -> list[str]:
        if self.selected_state:
            state_abbr = state_to_abbr_dict[self.selected_state]
            return sorted(cities_by_state.get(state_abbr))
        else:
            return []

    def event_state_state_selected(self, selection: str) -> None:
        self.selected_state = selection
        self.selected_city = ""

    def event_state_city_selected(self, selection: str) -> None:
        self.selected_city = selection

    def event_state_search(self) -> Iterable[Callable]:
        """
        Ensure that everything is properly selected, as well as
        prevent user from triggering search button unless a new
        selection is made.
        """
        try:
            if not self.selected_state:
                return rx.toast.error("State and city must be selected.")
            if not self.selected_city:
                return rx.toast.error("A city must be selected.")
            if (
                self.selected_state
                and self.selected_city
                and not (
                    self.selected_state == self.last_searched_state
                    and self.selected_city == self.last_searched_city
                )
            ):
                # Clear last search results.
                self.search_results = []

                # Get results from database.
                search_results = supabase_get_hospital_search_results(
                    self.access_token,
                    state_to_abbr_dict[self.selected_state],
                    self.selected_city,
                )

                # Set the last searched state/city
                self.last_searched_state = self.selected_state
                self.last_searched_city = self.selected_city

                # Format the city as title
                for hospital in search_results:
                    hospital["hosp_city"] = hospital["hosp_city"].title()

                # Set the results to state.
                self.search_results = search_results

        except Exception as e:
            logger.warning(e)
            yield rx.toast.error("Failed to retrieve search results.")

    def clear_search_results(self) -> None:
        self.selected_city = ""
        self.selected_state = ""
        self.search_results = []
