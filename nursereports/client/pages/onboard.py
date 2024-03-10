
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.lists import years_experience
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.onboard import OnboardState

import reflex as rx

@rx.page(
        route="/onboard",
        title="Nurse Reports",
        on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def onboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='80px'),
        content(),
        spacer(height='80px'),
        footer(),
        width='100%',
        flex_direction='column',
        justify="start",
        align_items='center',
        min_height='100vh'
    )

def content() -> rx.Component:
    return rx.flex(
        rx.flex(
            header_image(),
            first_panel(),
            gap='20px',
            flex_direction=['column', 'column', 'row', 'row', 'row']
        ),
        second_panel(),
        gap='40px',
        padding_x='20px',
        width=['100%', '100%', '800px', '800px', '800px'],
        align='center',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def header_image() -> rx.Component:
    return rx.flex(
        rx.text(
            "onboard_image"
        ),
        width='100%',
        padding='100px 0px 100px 0px',
        border='1px dashed black',
        align_items='center',
        justify_content='center'
    )

def first_panel() -> rx.Component:
    return rx.flex( 
        rx.vstack(
            rx.heading(
                "Thanks for joining us!",
                width='100%'
            ),
            rx.text(
                """
                Hey, I'm Jeremy, a current bedside ICU nurse
                from the East Coast. I started building this site
                after watching
                hospitals ignore the needs of the nursing community
                during COVID. To read more about
                our lofty goals and what makes this project special
                """,
                rx.link("click here.")
            ),
            rx.text(
                """
                Our community is and always will be free to access. 
                I simply ask that you share a report first. If you
                are a student, or haven't worked bedside within the
                past year check the box below. You may still access
                our site but will need to submit a report once you
                are hired.
                """
            ),
            gap="20px",
        ),
        width='100%',
        justify='center'
    )

def second_panel() -> rx.Component:
    return rx.flex(
        rx.form(
            rx.vstack(
                rx.center(
                    rx.checkbox(
                        name='no_recent_experience',
                        default_checked=False,
                    ),
                    rx.text(
                        "I don't have ",
                        rx.popover.root(
                            rx.popover.trigger(
                                rx.link(
                                    "recent hospital experience",
                                    color_scheme='blue',
                                    size='2'
                                ),
                            ),
                            rx.popover.content(
                                rx.text(
                                    """Working in a bedside role within
                                    the past 1 year."""
                                )
                            )
                        ),
                        size='2'
                    ),
                    gap='8px',
                ),
                rx.button(
                    "Let's go!",
                    color_scheme='crimson',
                    type='submit'
                ),
                width='100%',
                gap='24px',
                align='center',
            ),
            width='100%',
            on_submit=OnboardState.event_state_submit_onboard
        ),
        width='100%'
    )