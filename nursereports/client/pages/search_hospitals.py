from ..components import (
    flex,
    footer,
    hospital_item_search,
    login_protected,
    navbar,
    text
    )

from ...states import BaseState, SearchState, UserState

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
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center min-h-screen",
    )


def content() -> rx.Component:
    return rx.flex(
        search(),
        search_results(),
        class_name="flex-col flex-grow items-center space-y-4 md:space-y-12 px-4 py-4 md:py-20 w-full max-w-screen-md h-full"
    )


def search() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                text("Search for Hospital", class_name="text-2xl font-bold"),
                class_name="flex-row items-center space-x-2"
            ),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-4 w-full"
        ),
        rx.flex(
            search_filters(),
            class_name="w-full"
        ),
        class_name="flex-col border rounded shadow-lg divide-y dark:divide-zinc-700 bg-zinc-100 w-full",
    )


def search_filters() -> rx.Component:
    return flex(
        callout(),
        flex(
            rx.flex(
                rx.select(
                    SearchState.state_options,
                    value=SearchState.selected_state,
                    placeholder="- Select state -",
                    position="popper",
                    size="3",
                    color_scheme="teal",
                    on_change=SearchState.event_state_state_selected,
                    width="100%"
                ),
                class_name="w-full"
            ),
            rx.flex(
                rx.select(
                    SearchState.city_options,
                    placeholder="- Select city -",
                    value=SearchState.selected_city,
                    position="popper",
                    size="3",
                    color_scheme="teal",
                    disabled=~SearchState.selected_state,
                    on_change=SearchState.event_state_city_selected,
                    width="100%"
                ),
                class_name="w-full"
            ),
            class_name="flex-row p-4 space-x-4 w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("x", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    text("Clear selection", class_name="font-bold select-none"),
                    on_click=[
                        SearchState.set_selected_state(""),
                        SearchState.set_selected_city(""),
                        SearchState.set_search_results([]),
                    ],
                    class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                ),
                class_name="flex-col w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75"
            ),
            rx.flex(
                rx.flex(
                    rx.icon("search", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    text("Search", class_name="font-bold select-none"),
                    on_click=[
                        SearchState.set_search_is_loading(True),
                        SearchState.event_state_search,
                        SearchState.set_search_is_loading(False),
                    ],
                    class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
                ),
                class_name="flex-col w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75"
            ),
            class_name="flex-row divide-x dark:divide-zinc-700 w-full"
        ),
        class_name="flex-col items-center divide-y dark:divide-zinc-700 w-full",
    )


def search_results() -> rx.Component:
    return flex(
        rx.cond(
            SearchState.search_is_loading,
            rx.flex(
                rx.icon("loader-circle", class_name="animate-spin stroke-zinc-700 dark:stroke-zinc-500"),
                class_name="flex-col items-center justify-center min-h-24 w-full",
            ),
            rx.cond(
                SearchState.search_results,
                # Search results present.
                rx.flex(
                    rx.foreach(SearchState.search_results, hospital_item_search),
                    class_name="flex-col divide-y dark:divide-zinc-700 w-full",
                ),
                # No search results present.
                rx.flex(
                    rx.icon("ellipsis", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex-col items-center justify-center min-h-24 w-full",
                ),
            ),
        ),
        class_name="flex-col border rounded shadow-lg bg-zinc-100 w-full",
    )

def callout() -> rx.Component:
    return rx.cond(
        UserState.user_needs_onboarding,
        rx.flex(
            rx.callout(
                "Please provide a report before accessing our resources. Select your hospital using the dropdowns below.",
                icon="info",
                class_name="w-full"
            ),
            class_name="p-4 w-full"
        )
    )
