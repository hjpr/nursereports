from ..client.components.dicts import state_to_abbr_dict
from ..states.auth_state import AuthState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class SearchState(AuthState):
    # ---------------------------------------------------------------------------
    # Vars
    # ---------------------------------------------------------------------------
    search_query: str = ""
    search_suggestions: list[dict] = []  # top-5 live autocomplete
    suggestions_visible: bool = False
    current_search_page: int = 1
    _search_page_size: int = 10

    @rx.var
    def paginated_search_results(self) -> list[dict]:
        start = (self.current_search_page - 1) * self._search_page_size
        return self.search_results[start : start + self._search_page_size]

    @rx.var
    def num_search_pages(self) -> int:
        if not self.search_results:
            return 1
        return (len(self.search_results) + self._search_page_size - 1) // self._search_page_size

    search_is_loading: bool = False
    quick_search_is_loading: bool = False
    search_results: list[dict]

    @rx.var(cache=True)
    def state_options(self) -> list[str]:
        """Used by onboard.py state dropdown."""
        return [state for state in state_to_abbr_dict.keys()]

    # ---------------------------------------------------------------------------
    # Text-search helpers
    # ---------------------------------------------------------------------------

    def _text_search(self, query: str, limit: int) -> list[dict]:
        """
        Return up to `limit` hospitals matching `query`.
        Priority: hospital name matches first, then city matches to fill remainder.
        Results are deduplicated by hosp_id.
        """
        cols = "hosp_name,hosp_city,hosp_state,hosp_id,hosp_addr"

        # Step 1 — name matches
        name_results: list[dict] = (
            self.query()
            .table("hospitals_v2")
            .ilike("hosp_name", f"%{query}%")
            .select(cols)
            .execute()
        )[:limit]

        # Step 2 — fill remainder from city matches (deduplicated)
        if len(name_results) < limit:
            needed = limit - len(name_results)
            seen = {h["hosp_id"] for h in name_results}
            city_results: list[dict] = (
                self.query()
                .table("hospitals_v2")
                .ilike("hosp_city", f"%{query}%")
                .select(cols)
                .execute()
            )
            for h in city_results:
                if h["hosp_id"] not in seen and needed > 0:
                    name_results.append(h)
                    needed -= 1

        # Normalize casing
        for h in name_results:
            h["hosp_city"] = h["hosp_city"].title()
            h["hosp_addr"] = h["hosp_addr"].title()

        return name_results

    # ---------------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------------

    async def event_state_update_query(self, value: str):
        """Update search query and refresh autocomplete suggestions."""
        self.search_query = value
        if len(value) < 2:
            self.search_suggestions = []
            self.suggestions_visible = False
            self.quick_search_is_loading = False
            return
        self.quick_search_is_loading = True
        yield
        try:
            results = self._text_search(value, limit=5)
            self.search_suggestions = results
            self.suggestions_visible = bool(results)
        except Exception as e:
            logger.warning(f"Suggestion fetch failed: {e}")
            self.search_suggestions = []
            self.suggestions_visible = False
        finally:
            self.quick_search_is_loading = False

    def next_search_page(self) -> None:
        if self.current_search_page < self.num_search_pages:
            self.current_search_page += 1

    def previous_search_page(self) -> None:
        if self.current_search_page > 1:
            self.current_search_page -= 1

    def event_state_hide_suggestions(self) -> None:
        """Collapse the autocomplete dropdown."""
        self.suggestions_visible = False
        self.search_suggestions = []

    def event_state_full_search(self) -> Iterable[Callable]:
        """Run full search returning up to 20 results, then clear suggestions."""
        try:
            if len(self.search_query) < 2:
                return rx.toast.error("Please enter at least 2 characters.")
            self.search_is_loading = True
            self.suggestions_visible = False
            self.search_suggestions = []
            self.current_search_page = 1
            self.search_results = self._text_search(self.search_query, limit=20)
        except Exception as e:
            logger.warning(f"Full search failed: {e}")
            yield rx.toast.error("Failed to retrieve search results.")
        finally:
            self.search_is_loading = False

    def event_state_clear_search(self) -> None:
        """Clear all search state."""
        self.search_query = ""
        self.search_suggestions = []
        self.suggestions_visible = False
        self.search_results = []
        self.current_search_page = 1

