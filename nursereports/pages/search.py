
from ..components.custom import spacer
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer
from ..states.search import SearchState

import reflex as rx
        
def search() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
         rx.flex(
            # SEARCH SELECT CONTAINER
            rx.vstack(
                rx.heading(
                    "Find your hospital",
                    size='md',
                    ),
                spacer(height='20px'),
                rx.hstack(
                    rx.select(
                        SearchState.state_options,
                        value=SearchState.selected_state,
                        placeholder="Select state",
                        id="selected_state",
                        on_change=SearchState.do_selected_state
                    ),
                    rx.select(
                       SearchState.city_options,
                        placeholder="Select city",
                        value=SearchState.selected_city,
                        id="selected_city",
                        on_change=SearchState.do_selected_city
                    ),
                    width=['100%', '100%', '600px', '600px', '600px'],
                ),
                rx.accordion(
                    rx.accordion_item(
                        rx.accordion_button(
                            rx.text("Filters"),
                            rx.accordion_icon()
                        ),
                        rx.accordion_panel(
                            rx.center(
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
                        )
                    ),
                    allow_toggle=True,
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
        SearchState.search_results,
        rx.vstack(
            rx.foreach(
                SearchState.search_results,
                render_results
            ),
            width='100%',
            spacing='1em'
        )
    )

def render_results(result: dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        f"{result['hosp_name']}",
                        size='md'
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
                        color_scheme='teal',
                        on_click=SearchState.nav_to_report(result['hosp_id']),
                        is_loading=~rx.State.is_hydrated
                    ),
                    width='30%',
                    justify='flex-end',
                ),
                # STYLING FOR HSTACK CONTAINER INSIDE FLEX
                width='100%',
                spacing='3em',
            ),
            # STYLING FOR FLEX CONTAINER INSIDE CARD
            flex_direction='row'
        ),
        # STYLING FOR CARD
        width='100%',
    )