
from ..components.c2a import c2a
from ..components.custom import spacer
from ..components.footer import footer
from ..components.navbar import navbar
from ..states.search import SearchState

import reflex as rx
        
def search() -> rx.Component:
    return rx.flex(

        c2a(),

        navbar(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
         rx.flex(
            # SEARCH SELECT CONTAINER
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

                # STYLING FOR SEARCH SELECT CONTAINER
                width=['100%', '100%', '600px', '600px', '600px'],
            ),

            # STYLING FOR MAIN CONTENT CONTAINER
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

        # STYLING FOR PAGE BODY
        width='100%',
        flex_direction='column',
        align='center',
        min_height='100vh',
    )

def search_results() -> rx.Component:
    return rx.cond(
        rx.State.is_hydrated,
        # STATE HYDRATED TRUE
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
        # STATE HYDRATED FALSE
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
                # STYLING FOR HSTACK CONTAINER INSIDE FLEX
                width='100%',
            ),
            # STYLING FOR FLEX CONTAINER INSIDE CARD
            flex_direction='row'
        ),
        # STYLING FOR CARD
        width='100%',
    )