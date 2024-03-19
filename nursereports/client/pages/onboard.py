
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.lists import years_experience
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.onboard import OnboardState
from ...states.search import SearchState

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
        align_items='center',
        justify_content='center',
        min_height='100vh'
    )

def content() -> rx.Component:
    return rx.flex(
        header_image(),
        greeting(),
        questions(),
        button(),
        callout_error(),
        gap='24px',
        flex_direction='column',
        padding_x='20px',
        width=['100%', '480px', '480px', '480px', '480px'],
        align='center',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def header_image() -> rx.Component:
    return rx.flex(
        rx.text(
            "placeholder"
        ),
        width='100%',
        padding='100px 0px 100px 0px',
        border='1px dashed black',
        align_items='center',
        justify_content='center'
    )

def greeting() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Thanks for joining!",
                width='100%'
            ),
            rx.divider(),
        ),
        spacer(height='8px'),
        rx.flex( 
            rx.vstack(
                rx.text(
                    """
                    Hey, I'm Jeremy, a current bedside ICU nurse
                    from the East Coast. I built this tool to help
                    nurses share hospital information from across
                    the US.
                    """,
                ),
                rx.text(
                    """
                    This community will always be free to access,
                    I simply ask that you share a report first.
                    """
                )
            ),
            flex_direction='column',
            width='100%'
        )
    )

def questions() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.vstack(
                rx.text(
                    "Are you licensed?"
                ),
                rx.select(
                    ["APRN", "RN - Bachelors", "RN - Associates", "LPN/LVN", "Nursing Student"],
                    placeholder="- Select one -",
                    value=OnboardState.license,
                    on_change=OnboardState.set_license,
                    required=True,
                    size='3',
                    width='100%'
                ),
                width='100%'
            ),
            rx.cond(
                OnboardState.license,
                rx.cond(
                    ~OnboardState.is_student,
                    rx.flex(
                        rx.vstack(
                            rx.text(
                                "What state are you licensed in?"
                            ),
                            rx.select(
                                SearchState.state_options,
                                placeholder="- Select one -",
                                value=OnboardState.license_state,
                                on_change=OnboardState.set_license_state,
                                required=True,
                                size='3',
                                width='100%'
                            ),
                            width='100%'
                        ),
                        rx.vstack(
                            rx.text(
                                """Have you worked in a hospital in some
                                nursing role within the past year?
                                """
                            ),
                            rx.select(
                                ["Yes", "No"],
                                placeholder="- Select one -",
                                value=OnboardState.has_review,
                                on_change=OnboardState.set_has_review,
                                required=True,
                                size='3',
                                width='100%'
                            ),
                            width='100%'
                        ),
                        flex_direction='column',
                        gap='24px',
                        width='100%'
                    )
                )
            ),
            rx.cond(
                ~OnboardState.can_give_review,
                callout_review()
            ),
            flex_direction='column',
            gap='24px',
            width='100%'
        ),
        width='100%'
    )

def button() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Let's go!",
                rx.icon('arrow-big-right'),
                variant='ghost',
                size='3',
                on_click=OnboardState.event_state_submit_onboard
            ),
            width='100%',
            justify_content='center'
        ),
        width='100%'
    )

def callout_review() -> rx.Component:
    return rx.callout(
        """Submit a review when you get hired (within the year)
        to maintain access. You won't be required to submit a
        report right now.
        """,
        icon='info',
        width='100%'
    )

def callout_error() -> rx.Component:
    return rx.flex(
        rx.cond(
            OnboardState.onboard_has_error,
            rx.callout(
                OnboardState.onboard_error_message,
                width='100%',
                icon='alert_triangle',
                color_scheme='red',
                role='alert'
            )
        ),
        width='100%'
    )