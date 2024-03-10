
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.search import SearchState
from typing import Dict

import reflex as rx
        
@rx.page(
        title="Search",
        route="/search/[context]",
        on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def search_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        content(),
        footer(),
        flex_direction='column',
        align='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        header(),
        search_dropdowns(),
        rx.divider(),
        search_results(),
        padding_x='20px',
        width='100%',
        max_width='768px',
        spacing='4',
        align='center',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def header() -> rx.Component:
    """url_context can be either 'hospital' or 'report'."""
    return rx.flex(
        rx.heading(
            "Find your hospital"
        ),
        width='100%',
        justify='center'
    )

def search_dropdowns() -> rx.Component:
    return rx.flex(
        rx.select(
            SearchState.state_options,
            value=SearchState.selected_state,
            placeholder="- Select state -",
            position='popper',
            on_change=SearchState.event_state_state_selected,
            width='40%'
        ),
        rx.select(
            SearchState.city_options,
            placeholder="- Select city -",
            value=SearchState.selected_city,
            position='popper',
            on_change=SearchState.event_state_city_selected,
            width='40%'
        ),
        rx.button(
            "Search",
            on_click=SearchState.event_state_search
        ),
        gap='8px',
        width='100%',
        justify_content='center'
    )

def search_results() -> rx.Component:
    return rx.cond(
        SearchState.search_results,
        rx.vstack(
            rx.foreach(
                SearchState.search_results,
                render_results
            ),
            width='100%',
            spacing='4'
        )
    )

def render_results(result: Dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        f"{result['hosp_name']}"
                        ),
                    rx.text(f"{result['hosp_addr']}, "\
                            f"{result['hosp_state']} "\
                            f"{result['hosp_zip']}"
                            ),
                    width='100%',
                    align_items='left'
                ),
                rx.flex(
                    rx.button(
                        "Select",
                        on_click=SearchState.nav_to_report(result['hosp_id']),
                    ),
                    height='100%',
                    width='30%',
                    justify='end',
                    align='center'
                ),
                width='100%',
            ),
            flex_direction='row'
        ),
        width='100%',
    )