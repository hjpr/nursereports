
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states import *
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
        spacer(height='56px'),
        content(),
        spacer(height='40px'),
        footer(),
        background='linear-gradient(ghostwhite, honeydew)',
        flex_direction='column',
        align='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        header(),
        search_dropdowns(),
        search_results(),
        padding_x='20px',
        width='100%',
        max_width='768px',
        gap='24px',
        align='center',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0'
    )

def header() -> rx.Component:
    return rx.flex(
        rx.heading(
            "Find your hospital",
            color='grey'
        ),
        width='100%',
        justify='center'
    )

def search_dropdowns() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.select(
                SearchState.state_options,
                value=SearchState.selected_state,
                placeholder="- Select state -",
                size='3',
                radius='full',
                position='popper',
                on_change=SearchState.event_state_state_selected,
                width=['100%', '40%', '40%', '40%', '40%']
            ),
            rx.select(
                SearchState.city_options,
                placeholder="- Select city -",
                value=SearchState.selected_city,
                size='3',
                radius='full',
                position='popper',
                on_change=SearchState.event_state_city_selected,
                width=['100%', '40%', '40%', '40%', '40%']
            ),
            rx.button(
                "Search",
                on_click=[
                    SearchState.set_search_is_loading(True),
                    SearchState.set_search_results([]),
                    SearchState.event_state_search,
                    SearchState.set_search_is_loading(False)
                ],
                size='3',
                radius='full'
            ),
            flex_direction=['column', 'row', 'row', 'row', 'row'],
            gap=['12px', '8px', '8px', '8px', '8px'],
            width='100%',
            justify_content='center'
        ),
        rx.divider(),
        width='100%',
        flex_direction='column',
        gap='24px'
    )

def search_results() -> rx.Component:
    return rx.flex(
        rx.cond(
            SearchState.search_results,
            rx.flex(
                rx.foreach(
                    SearchState.search_results,
                    render_results
                ),
                flex_direction='column',
                width='100%',
                spacing='4'
            ),
            rx.flex(
                rx.cond(
                    SearchState.search_is_loading,
                    rx.chakra.spinner(),
                    rx.icon('search', color='teal'),
                ),
                width='100%',
                align_items='center',
                justify_content='center'
            )
        ),
        min_height='300px',
        width='100%',
        flex_grow='1'
    )

def render_results(result: Dict) -> rx.Component:
    return rx.flex(
        rx.hstack(
            rx.flex(
                rx.heading(
                    f"{result['hosp_name']}",
                    size='3'
                ),
                rx.text(f"{result['hosp_addr']}"),
                rx.text(f"{result['hosp_city']}, \
                    {result['hosp_state']}\
                    {result['hosp_zip']}"
                ),
                flex_direction='column',
                width='100%',
                gap='4px'
            ),
            rx.flex(
                rx.button(
                    "Select",
                    rx.icon('chevron-right'),
                    size='3',
                    radius='full',
                    on_click=SearchState.nav_to_report(result['hosp_id'])
                ),
                height='100%',
                width='30%',
                justify='end',
                align='center'
            ),
            width='100%',
        ),
        flex_direction='row',
        width='100%',
        justify_content='space-between',
        padding='0 0 24px 0'
    )