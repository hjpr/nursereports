
from ..components.c2a import c2a
from ..components.custom import spacer
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.search import SearchState

import reflex as rx
        
@rx.page(
        title="Search",
        route="/search/[context]",
        on_load=BaseState.standard_flow('req_login')
)
def search_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
         rx.flex(
            rx.vstack(
                rx.heading(
                    "Find your hospital",
                    ),
                spacer(height='20px'),
                rx.hstack(
                    rx.select(
                        SearchState.state_options,
                        value=SearchState.selected_state,
                        placeholder="Select state",
                        on_change=SearchState.do_selected_state
                    ),
                    rx.select(
                       SearchState.city_options,
                        placeholder="Select city",
                        value=SearchState.selected_city,
                        on_change=SearchState.do_selected_city
                    ),
                    width=['100%', '100%', '600px', '600px', '600px'],
                ),
                rx.accordion.root(
                    rx.accordion.item(
                        header="Filters",
                        content=rx.center(
                            rx.text(
                                "Max results per page",
                                width='100%'
                                ),
                            rx.spacer(),
                            rx.select(
                                SearchState.range_options,
                                on_change=SearchState.set_current_search_range,
                            )
                        )
                    ),
                    width='100%'
                ),
                spacer(height='40px'),
                search_results(),
                spacer(height='80px'),
                width=['100%', '100%', '600px', '600px', '600px'],
            ),
            padding_x='20px',
            width='100%',
            max_width='1200px',
            align='center',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
        ),
        footer(),
        width='100%',
        flex_direction='column',
        align='center',
        min_height='100vh',
    )

def search_results() -> rx.Component:
    return rx.cond(
        rx.State.is_hydrated,
        rx.cond(
            SearchState.search_results,
            rx.cond(
                ~SearchState.results_failed,
                rx.vstack(
                    rx.foreach(
                        SearchState.search_results,
                        render_results
                    ),
                    width='100%',
                ),
                rx.center(
                    rx.text("Your token has expired, please refresh this page to login again."),
                    width='100%'
                )
            )
        ),
        rx.chakra.spinner()
    )

def render_results(result: dict) -> rx.Component:
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
                    width='30%',
                    justify='end',
                ),
                width='100%',
            ),
            flex_direction='row'
        ),
        width='100%',
    )