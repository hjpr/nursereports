
from ..components.c2a import c2a
from ..components.custom import spacer
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.navbar import NavbarState

import reflex as rx

@rx.page(
        route='/',
        title='Nurse Reports',
        on_load=BaseState.event_state_standard_flow('none')
)
def index_page() -> rx.Component:
    return rx.flex(
        rx.theme_panel(default_open=False),
        c2a(),
        navbar(),
        content(),
        footer(),
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        main_panel(),
        first_panel(),
        rx.divider(max_width='728px'),
        second_panel(),
        rx.divider(max_width='728px'),
        third_panel(),
        rx.divider(max_width='728px'),
        fourth_panel(),
        spacer(height='16px'),
        width='100%',
        spacing='8',
        align='center',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def main_panel() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading(
                    """Management has pizza covered, we'll give you
                    everything else.""",
                    font_size=["35px", "35px", "60px", "60px", "60px"],
                    letter_spacing=["-0.01em", "-0.01em", "-0.025em", "-0.025em", "-0.025em"],
                    line_height=["40px", "40px", "60px", "60px", "60px"],
                    color_scheme="crimson"
                ),
                rx.heading(
                    """From fair wages, to unit insights - submit,
                    search and compare hospital reviews across the US. 
                    All it costs is a report of your own.
                    """,
                    size='6',
                    font_size=["20px", "20px", "24px", "24px", "24px"],
                    letter_spacing=["-0.005em", "-0.005em", "-0.00625em", "-0.00625em", "-0.00625em"],
                    line_height=["28px", "28px", "30px", "30px", "30px"],

                ),
                rx.divider(),
                rx.button(
                    "Sign up for access.",
                    color_scheme='crimson',
                    on_click=NavbarState.event_state_c2a_main
                ),
                gap=["1em","1em","2em", "2em", "2em"]
            ),
            padding='24px',
            max_width='768px',
            box_shadow='0px 4px 5px -5px rgba(0, 0, 0, 0.5)'
        ),
        padding='24px',
        background='url(/vector/pizzabg.svg)',
        background_size='cover',
        width='100%'
    )

def first_panel() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                """Discover information on pay, benefits, staffing,
                and culture across hospitals nationwide.""",
                size='8',
                text_align='center'
            )
        ),
        width='100%',
        max_width='768px',
        padding_x='24px'
    )

def second_panel() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                "The most important 5 minutes of your career."
            ),
            rx.text(
                """
                Understanding the state of nursing both locally and
                nationwide requires coordinated communication. Learn
                vital details from a structured report about pay,
                benefits, ratios, culture and much more.
                """
            ),
            width='100%'  
        ),
        rx.box(
            height='200px',
            width='100%',
            border='1px dashed black'
        ),
        gap='12px',
        flex_direction=['column', 'row', 'row', 'row', 'row'],
        align_items='center',
        justify_content='center',
        width='100%',
        max_width='768px',
        padding_x='24px'
    )

def third_panel() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                "Speak freely and anonymously."
            ),
            rx.text(
                """
                Submit reports without fear of blowback.
                Your personal information won't be shared
                with hospitals or any other third party.
                """
            ),
            width='100%'  
        ),
        rx.box(
            height='200px',
            width='100%',
            border='1px dashed black'
        ),
        gap='12px',
        flex_direction=['column', 'row', 'row', 'row', 'row'],
        align_items='center',
        justify_content='center',
        width='100%',
        max_width='768px',
        padding_x='24px'
    )

def fourth_panel() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.box(
                height='200px',
                width='100%',
                border='1px dashed black'
            ),
            rx.box(
                height='200px',
                width='100%',
                border='1px dashed black'
            ),
            width='100%',
            justify='center'
        ),
        width='100%',
        max_width='768px'
    )