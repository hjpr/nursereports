from ...components import (
    button,
    heading,
    text,
    icon,
    login_protected,
)
from .navbar import navbar
from ....states import BaseState, HospitalState, ReportState, SearchState, UserState

import reflex as rx

@rx.page(
    title="Search",
    route="/search/hospital",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
    ],
)
@login_protected
def search_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        _search_card(),
        _results_list(),
        class_name=(
            "flex-col flex-1 justify-start gap-4 "
            "w-full max-w-screen-md "
            "mx-auto px-4 md:px-8 pt-[12vh] pb-10"
        ),
    )


# ---------------------------------------------------------------------------
# Search card
# ---------------------------------------------------------------------------

def _search_card() -> rx.Component:
    return rx.flex(
        # Card header
        rx.flex(
            rx.box(
                class_name=(
                    "absolute inset-0 "
                    "pointer-events-none"
                ),
            ),
            icon("search", accent=True, class_name="h-5 w-5 relative"),
            heading("Find a Hospital", size="sm", class_name="relative"),
            class_name=(
                "relative flex-row items-center gap-2 "
                "px-5 py-4 overflow-hidden bg-emerald-500/10 dark:bg-white/[0.03] "
                "border-b border-neutral-300 dark:border-neutral-800/50"
            ),
        ),
        # Card body
        rx.flex(
            _onboarding_callout(),
            _search_input_row(),
            class_name="flex-col gap-4 p-5",
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-visible"
        ),
    )


def _onboarding_callout() -> rx.Component:
    return rx.cond(
        UserState.user_needs_onboarding,
        rx.flex(
            icon("info", accent=True, class_name="h-4 w-4 shrink-0 mt-0.5"),
            text(
                "Please submit a report before accessing hospital data. "
                "Search for your hospital below to get started.",
                size="sm",
            ),
            class_name=(
                "flex-row gap-3 items-start "
                "bg-emerald-50 dark:bg-emerald-900/20 "
                "border border-emerald-300 dark:border-emerald-800 "
                "rounded-xl p-4"
            ),
        ),
        rx.fragment(),
    )


def _search_input_row() -> rx.Component:
    """Input field + inline Search button on same row. Dropdown sits below input only."""
    return rx.flex(
        # Left: input with absolute dropdown
        rx.box(
            rx.flex(
                rx.debounce_input(
                    rx.input(
                        placeholder="Search by hospital name or city…",
                        value=SearchState.search_query,
                        on_change=SearchState.event_state_update_query,
                        on_key_up=rx.cond(
                            rx.Var.create("event.key") == "Enter",
                            SearchState.event_state_full_search,
                            rx.noop(),
                        ),
                        class_name=(
                            "flex-1 min-w-0 p-0 bg-transparent outline-none "
                            "border-0 shadow-none ring-0 "
                            "text-sm text-neutral-900 dark:text-neutral-100 "
                            "placeholder:text-neutral-400 dark:placeholder:text-neutral-600"
                        ),
                    ),
                    debounce_timeout=300,
                ),
                # Inline clear / loading indicator
                rx.cond(
                    SearchState.search_is_loading | SearchState.quick_search_is_loading,
                    rx.spinner(size="1", class_name="shrink-0"),
                    rx.cond(
                        SearchState.search_query != "",
                        rx.el.button(
                            icon("x", muted=True, class_name="h-4 w-4"),
                            on_click=SearchState.event_state_clear_search,
                            class_name=(
                                "flex items-center justify-center shrink-0 "
                                "hover:text-neutral-700 dark:hover:text-neutral-300 "
                                "transition-colors cursor-pointer"
                            ),
                        ),
                        rx.fragment(),
                    ),
                ),
                class_name=(
                    "flex-row items-center gap-3 "
                    "bg-white dark:bg-white/[0.06] "
                    "border border-neutral-300 dark:border-neutral-700 "
                    "rounded-xl px-3 py-2 "
                    "focus-within:border-emerald-400 dark:focus-within:border-emerald-700 "
                    "transition-colors"
                ),
            ),
            # Dropdown — z-50 sits above backdrop (z-40)
            rx.cond(
                SearchState.suggestions_visible,
                rx.flex(
                    rx.foreach(SearchState.search_suggestions, _suggestion_row),
                    class_name=(
                        "flex-col "
                        "absolute left-0 right-0 top-[calc(100%+4px)] "
                        "bg-emerald-100 dark:bg-[#0f1f13] "
                        "border border-neutral-200 dark:border-neutral-800/50 "
                        "rounded-xl shadow-lg dark:shadow-black/40 "
                        "overflow-hidden z-50"
                    ),
                ),
                rx.fragment(),
            ),
            class_name="relative flex-1 min-w-0",
        ),
        # Right: Search button — always visible, never covered
        button(
            icon("search", class_name="h-4 w-4"),
            "Search",
            color="emerald",
            size="md",
            loading=SearchState.search_is_loading,
            on_click=SearchState.event_state_full_search,
        ),
        class_name="flex-row items-center gap-3 w-full",
    )


def _suggestion_row(hospital: dict) -> rx.Component:
    return rx.flex(
        # Hospital info
        rx.flex(
            rx.skeleton(
                text(hospital["hosp_name"], weight="medium", class_name="truncate"),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                rx.text(
                    hospital["hosp_addr"],
                    class_name="text-xs text-neutral-500 truncate",
                ),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                rx.text(
                    hospital["hosp_city"],
                    ", ",
                    hospital["hosp_state"],
                    class_name="text-xs text-neutral-500 truncate",
                ),
                loading=~rx.State.is_hydrated,
            ),
            class_name="flex-col flex-1 min-w-0 justify-center px-4 py-3",
        ),
        # Actions
        rx.flex(
            rx.cond(
                ~UserState.user_needs_onboarding,
                rx.flex(
                    rx.skeleton(
                        rx.tooltip(
                            icon("bookmark-plus", muted=True, class_name="h-5 w-5"),
                            content="Save hospital",
                        ),
                        loading=~rx.State.is_hydrated,
                    ),
                    on_click=UserState.event_state_add_hospital(hospital["hosp_id"]),
                    class_name=(
                        "flex items-center justify-center "
                        "w-12 self-stretch "
                        "hover:bg-neutral-200/60 dark:hover:bg-white/[0.04] "
                        "transition-colors duration-150 cursor-pointer"
                    ),
                ),
                rx.fragment(),
            ),
            rx.flex(
                rx.skeleton(
                    icon("arrow-right", muted=True, class_name="h-5 w-5"),
                    loading=~rx.State.is_hydrated,
                ),
                on_click=rx.cond(
                    UserState.user_needs_onboarding,
                    ReportState.event_state_create_full_report(hospital["hosp_id"]),
                    HospitalState.redirect_to_hospital_overview(hospital["hosp_id"]),
                ),
                class_name=(
                    "flex items-center justify-center "
                    "w-12 self-stretch "
                    "hover:bg-neutral-200/60 dark:hover:bg-white/[0.04] "
                    "transition-colors duration-150 cursor-pointer"
                ),
            ),
            class_name="flex-row self-stretch",
        ),
        class_name=(
            "flex-row items-center justify-between "
            "min-h-[72px] "
            "border-b border-neutral-300 dark:border-neutral-800/50 last:border-0"
        ),
    )


# ---------------------------------------------------------------------------
# Results — flat list below search card, no wrapper card
# ---------------------------------------------------------------------------

def _results_list() -> rx.Component:
    return rx.cond(
        SearchState.search_is_loading,
        rx.flex(
            icon("loader-circle", muted=True, class_name="h-6 w-6 animate-spin"),
            class_name="flex items-center justify-center py-10",
        ),
        rx.cond(
            SearchState.search_results,
            rx.flex(
                # Count line
                rx.text(
                    SearchState.search_results.length(),
                    " result",
                    rx.cond(SearchState.search_results.length() == 1, "", "s"),
                    " found",
                    class_name=(
                        "text-xs text-neutral-400 dark:text-neutral-600 "
                        "px-1 pb-1"
                    ),
                ),
                # Rows + pagination
                rx.flex(
                    rx.foreach(SearchState.paginated_search_results, _result_row),
                    rx.cond(
                        SearchState.num_search_pages > 1,
                        _pagination(),
                    ),
                    class_name=(
                        "flex-col divide-y divide-neutral-300 dark:divide-neutral-800/50 "
                        "bg-emerald-500/20 dark:bg-white/[0.03] "
                        "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
                        "rounded-2xl overflow-hidden"
                    ),
                ),
                class_name="flex-col gap-1 w-full",
            ),
            rx.fragment(),
        ),
    )


def _pagination() -> rx.Component:
    return rx.flex(
        rx.flex(
            icon("arrow-left", muted=True, class_name="h-4 w-4"),
            on_click=SearchState.previous_search_page,
            class_name=(
                "flex items-center justify-center flex-1 py-3 "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                "transition-colors duration-150 cursor-pointer"
            ),
        ),
        rx.flex(
            rx.text(
                SearchState.current_search_page,
                " / ",
                SearchState.num_search_pages,
                class_name="text-sm text-neutral-400 dark:text-neutral-600",
            ),
            class_name="flex items-center justify-center flex-1 py-3",
        ),
        rx.flex(
            icon("arrow-right", muted=True, class_name="h-4 w-4"),
            on_click=SearchState.next_search_page,
            class_name=(
                "flex items-center justify-center flex-1 py-3 "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                "transition-colors duration-150 cursor-pointer"
            ),
        ),
        class_name=(
            "flex-row "
            "divide-x divide-neutral-200 dark:divide-neutral-800/50 "
            "border-t border-neutral-200 dark:border-neutral-800/50"
        ),
    )


def _result_row(hospital: dict) -> rx.Component:
    return rx.flex(
        # Hospital info
        rx.flex(
            rx.skeleton(
                text(hospital["hosp_name"], weight="medium", class_name="truncate"),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                rx.text(
                    hospital["hosp_addr"],
                    class_name="text-sm text-neutral-500 truncate",
                ),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                rx.text(
                    hospital["hosp_city"],
                    ", ",
                    hospital["hosp_state"],
                    class_name="text-sm text-neutral-500 truncate",
                ),
                loading=~rx.State.is_hydrated,
            ),
            class_name="flex-col flex-1 min-w-0 justify-center gap-0.5",
        ),
        # Actions
        rx.flex(
            rx.cond(
                ~UserState.user_needs_onboarding,
                rx.flex(
                    rx.skeleton(
                        rx.tooltip(
                            icon("bookmark-plus", muted=True, class_name="h-5 w-5"),
                            content="Save hospital",
                        ),
                        loading=~rx.State.is_hydrated,
                    ),
                    on_click=UserState.event_state_add_hospital(hospital["hosp_id"]),
                    class_name=(
                        "flex items-center justify-center "
                        "w-12 self-stretch "
                        "hover:bg-neutral-100 dark:hover:bg-neutral-800"
                        "transition-colors duration-150 cursor-pointer"
                    ),
                ),
                rx.fragment(),
            ),
            rx.flex(
                rx.skeleton(
                    icon("arrow-right", muted=True, class_name="h-5 w-5"),
                    loading=~rx.State.is_hydrated,
                ),
                on_click=rx.cond(
                    UserState.user_needs_onboarding,
                    ReportState.event_state_create_full_report(hospital["hosp_id"]),
                    HospitalState.redirect_to_hospital_overview(hospital["hosp_id"]),
                ),
                class_name=(
                    "flex items-center justify-center "
                    "w-12 self-stretch "
                    "hover:bg-neutral-100 dark:hover:bg-neutral-800"
                    "transition-colors duration-150 cursor-pointer"
                ),
            ),
            class_name="flex-row self-stretch",
        ),
        class_name=(
            "flex-row items-center justify-between "
            "px-5 py-3 min-h-[72px]"
        ),
    )
