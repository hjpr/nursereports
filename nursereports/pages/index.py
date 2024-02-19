
from ..components.footer import footer
from ..components.navbar import navbar, c2a_spacer

import reflex as rx

def index() -> rx.Component:
    return rx.flex(

        rx.theme_panel(default_open=False),

        navbar(),

        c2a_spacer(),

        # MAIN CONTENT CONTAINER
        rx.flex(

            main_panel(),

            first_panel(),

            second_panel(),

            third_panel(),

            # STYLING FOR CONTENT CONTAINER
            padding_x='40px',
            max_width='1200px',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
            
        ),

        footer(),

        # STYLING FOR BODY CONTAINER
        flex_direction='column',
        align_items='center',
        min_height='100vh',

    )

def main_panel() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading(
                    "Nursing just got an upgrade.",
                    size='9',
                    color_scheme="crimson"
                ),
                rx.heading(
                    """Submit, search, and compare hospitals across the
                    US. All it costs is a review of your own.
                    """,
                    size='6'
                ),
                rx.divider(),
                rx.button(
                    "Sign up for access."
                ),
                spacing='3',
            ),
            padding_x='64px',
            padding_y='12px',
            max_width='768px'
        ),
        height='600px'
    )

def first_panel() -> rx.Component:
    return rx.vstack(
        rx.heading(
            """The first comprehensive hospital report system for nurses,
            by nurses."""
            ),
        rx.text(
            """Nursereports.org is a RN-developed, community-provided 
            repository of hospital reports, to solely benefit nurses
            by finding the jobs we want with the pay we deserve. 
            """
        ),
        max_width='768px'
    )

def second_panel() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                "The most important 5 minutes of your career."
            ),
            rx.text(
                """
                Share details about pay, benefits, and workplace
                culture using our short but detailed reporting
                system.
                """
            )
        ),
        max_width='768px'
    )

def third_panel() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                "The most important 5 minutes of your career."
            ),
            rx.text(
                """
                Share details about pay, benefits, and workplace
                culture using our short but detailed reporting
                system.
                """
            )
        ),
        max_width='768px'
    )