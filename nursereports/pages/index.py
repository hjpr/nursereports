
from ..components.c2a import c2a
from ..components.footer import footer
from ..components.navbar import navbar
from ..components.custom import spacer

import reflex as rx

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
        rx.divider(max_width='768px'),
        second_panel(),
        rx.divider(max_width='768px'),
        third_panel(),
        rx.divider(max_width='768px'),
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
                    color_scheme='crimson'
                ),
                gap=["1em","1em","2em", "2em", "2em"]
            ),
            padding='48px',
            max_width='768px',
            box_shadow='0px 4px 5px -5px rgba(0, 0, 0, 0.5)'
        ),
        padding='40px',
        background='url(/vector/pizzabg.svg)',
        background_size='cover',
        width='100%'
    )

def first_panel() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                """The first comprehensive hospital report system for nurses,
                by nurses.""",
                size='8'
            ),
            rx.text(
                """We are a bedside-developed, community-built
                repository of hospital reports created to solely
                benefit the national nursing community. Our aim is
                twofold. First - create transparent communication
                to build better, more sustainable careers. Second -
                create a strong system of accountability which
                ensures that the nursing voice is heard whenever
                hospitals enact policies.
                """
            )
        ),
        width='100%',
        max_width='768px',
        padding_x='20px'
    )

def second_panel() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "The most important 5 minutes of your career."
                ),
                rx.text(
                    """
                    Our reporting process was designed to capture a
                    wide range of information while still taking
                    as little of your time as possible. Reports 
                    include details on pay and benefits, staffing
                    ratios, and even unit culture.
                    """
                ),
                width='100%'  
            ),
            rx.box(
                height='200px',
                width='100%',
                border='1px dashed black'
            ),
            align='center',
        ),
        width='100%',
        max_width='768px',
        padding_x='20px'
    )

def third_panel() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Always anonymous, free forever."
                ),
                rx.text(
                    """
                    Building a system of accountability that will
                    benefit us all requires trust. We hold that
                    trust sacred and don't provide your personal
                    information to any third party for any reason.
                    """
                ),
                width='100%'  
            ),
            rx.box(
                height='200px',
                width='100%',
                border='1px dashed black'
            ),
            align='center',
        ),
        width='100%',
        max_width='768px',
        padding_x='20px'
    )

def fourth_panel() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.box(
                height='200px',
                width='25%',
                border='1px dashed black'
            ),
            rx.box(
                height='200px',
                width='25%',
                border='1px dashed black'
            ),
            rx.box(
                height='200px',
                width='25%',
                border='1px dashed black'
            ),
            width='100%',
            justify='center'
        ),
        width='100%',
        max_width='768px'
    )