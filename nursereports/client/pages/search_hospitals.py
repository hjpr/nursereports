from ..components import (
    c2a,
    flex,
    footer,
    hospital_item_search,
    login_protected,
    navbar,
    solid_button,
    text
    )

from ...states import BaseState, SearchState

import reflex as rx


@rx.page(
    title="Search",
    route="/search/hospital",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
    ],
)
@login_protected
def search_page() -> rx.Component:
    return flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-teal-50",
    )


def content() -> rx.Component:
    return flex(
        header(),
        search_dropdowns(),
        search_results(),
        class_name="flex-col items-center px-4 py-12 w-full max-w-screen-md",
    )


def header() -> rx.Component:
    return flex(
        text("Find your hospital", class_name="text-2xl font-bold text-zinc-700"),
        class_name="flex-col items-center w-full",
    )


def search_dropdowns() -> rx.Component:
    return flex(
        flex(
            rx.select(
                SearchState.state_options,
                value=SearchState.selected_state,
                placeholder="- Select state -",
                position="popper",
                on_change=SearchState.event_state_state_selected,
                width=["100%", "100%", "30%", "30%", "30%"],
            ),
            rx.select(
                SearchState.city_options,
                placeholder="- Select city -",
                value=SearchState.selected_city,
                position="popper",
                disabled=~SearchState.selected_state,
                on_change=SearchState.event_state_city_selected,
                width=["100%", "100%", "30%", "30%", "30%"],
            ),
            solid_button(
                "Search",
                on_click=SearchState.event_state_search,
                loading=SearchState.search_is_loading,
                disabled=~(SearchState.selected_city & SearchState.selected_state),
                class_name="w-full md:w-auto disabled:cursor-not-allowed",
            ),
            solid_button(
                "Clear",
                disabled=~(SearchState.selected_state | SearchState.selected_city),
                on_click=[
                    SearchState.set_selected_state(""),
                    SearchState.set_selected_city(""),
                    SearchState.set_search_results([]),
                ],
                class_name="w-full md:w-auto disabled:cursor-not-allowed",
            ),
            class_name="flex-col md:flex-row items-center justify-center md:space-x-2 space-y-4 md:space-y-0 p-8 w-full",
        ),
        class_name="flex-col items-center space-y-4 w-full",
    )


def search_results() -> rx.Component:
    return flex(
        rx.cond(
            SearchState.search_results,
            # Search results present.
            flex(
                rx.foreach(SearchState.search_results, hospital_item_search),
                class_name="flex-col divide-y dark:divide-zinc-500 w-full",
            ),
            # No search results present.
            flex(
                rx.cond(
                    SearchState.search_is_loading,
                    rx.icon("loader-circle", class_name="animate-spin text-zinc-700"),
                    rx.icon("search", class_name="text-zinc-700"),
                ),
                class_name="flex-col items-center justify-center w-full",
            ),
        ),
        class_name="flex basis-80 grow w-full",
    )
