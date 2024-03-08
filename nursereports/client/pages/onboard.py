
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
        header_image(),
        first_panel(),
        second_panel(),
        gap='40px',
        padding_x='20px',
        width=['100%', '100%', '600px', '600px', '600px'],
        max_width='1200px',
        align='center',
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def header_image() -> rx.Component:
    return rx.center(
        rx.box(
            height="200px",
            width="300px",
            border='1px solid black'
        ),
        width="100%"
    )

def first_panel() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                "Thanks for joining us!",
                align="center",
                width='100%'
            ),
            rx.text(
                """
                Hey, I'm Jeremy, an active ICU nurse from the East
                Coast. I started this project after watching
                hospitals ignore the needs of the nursing community
                during COVID. If you want to read more about
                our lofty goals and what makes this project special
                """,
                rx.link("click here.")
            ),
            rx.text(
                """
                Our community is and always will be free to access - 
                I simply ask that you share a report first. Thanks!
                """
            ),
            gap="20px",
            max_width='400px',
            text_align='center',
        ),
        width='100%',
        justify='center'
    )

def second_panel() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.center(
                rx.checkbox(
                    name='create_account_student',
                    default_checked=False,
                ),
                rx.text(
                    "I'm a ",
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.link(
                                "nursing student.",
                                color_scheme='blue',
                                size='2'
                            ),
                        ),
                        rx.popover.content(
                            rx.text(
                                """Students can access our resources
                                for 1 year and then must submit a report
                                after hire to maintain access."""
                            )
                        )
                    ),
                    size='2'
                ),
                gap='8px',
            ),
            rx.button(
                "Let's go!"
            ),
            width='100%',
            gap='20px',
            align='center',
        ),
        width='100%',
    )