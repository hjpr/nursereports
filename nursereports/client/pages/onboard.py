from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base_state import BaseState
from ...states.onboard_state import OnboardState
from ...states.search_state import SearchState

import reflex as rx


@rx.page(
    route="/onboard",
    title="Nurse Reports",
    on_load=BaseState.event_state_standard_flow("login"),
)
@login_protected
def onboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        spacer(height="56px"),
        footer(),
        width="100%",
        background="linear-gradient(ghostwhite, honeydew)",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        greeting(),
        questions(),
        button(),
        gap="48px",
        flex_direction="column",
        padding_x="20px",
        width=["100%", "480px", "480px", "480px", "480px"],
        align="center",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def greeting() -> rx.Component:
    return rx.flex(
        spacer(height="56px"),
        rx.text(
            """Welcome to the community!""",
            font_size=["36px", "36px", "56px", "56px", "56px"],
            font_weight="bold",
            line_height=["1.1", "1.1", "1.2", "1.2", "1.2"],
            color_scheme="teal",
            text_align="center",
        ),
        rx.text(
            """
            Hey! I'm Jeremy. I'm an ICU nurse still working bedside
            on the East Coast. I built this tool to help nurses
            share hospital information across the US.
            """,
            text_align="center",
            line_height=["1.5", "1.5", "2", "2", "2"],
            color_scheme="gray",
        ),
        rx.text(
            """
            This community will always be free to access, I simply
            ask that you share a report first if you are currently
            working in a hospital.
            """,
            text_align="center",
            line_height=["1.5", "1.5", "2", "2", "2"],
            color_scheme="gray",
        ),
        flex_direction="column",
        gap="24px",
        width="100%",
        max_width=["480px", "480px", "640px", "640px", "640px"],
        padding="0px 12px",
    )


def questions() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.vstack(
                rx.text("Are you licensed?"),
                rx.select(
                    [
                        "APRN",
                        "RN - Bachelors",
                        "RN - Associates",
                        "LPN/LVN",
                        "Nursing Student",
                    ],
                    placeholder="- Select one -",
                    value=OnboardState.license,
                    on_change=OnboardState.set_license,
                    required=True,
                    size="3",
                    radius="full",
                    width="100%",
                ),
                width="100%",
            ),
            rx.cond(
                OnboardState.license,
                rx.cond(
                    ~OnboardState.is_student,
                    rx.flex(
                        rx.vstack(
                            rx.text("What state are you licensed in?"),
                            rx.select(
                                SearchState.state_options,
                                placeholder="- Select one -",
                                value=OnboardState.license_state,
                                on_change=OnboardState.set_license_state,
                                required=True,
                                size="3",
                                radius="full",
                                width="100%",
                            ),
                            width="100%",
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
                                size="3",
                                radius="full",
                                width="100%",
                            ),
                            width="100%",
                        ),
                        flex_direction="column",
                        gap="24px",
                        width="100%",
                    ),
                ),
            ),
            rx.cond(~OnboardState.can_give_review, callout_review()),
            callout_error(),
            flex_direction="column",
            gap="24px",
            width="100%",
        ),
        width="100%",
    )


def button() -> rx.Component:
    return rx.flex(
        rx.button(
            "Let's go!",
            rx.icon("chevron-right"),
            size="4",
            radius="full",
            border="4px solid gainsboro",
            on_click=OnboardState.event_state_submit_onboard,
        ),
        width="100%",
        justify_content="center",
    )


def callout_review() -> rx.Component:
    return rx.callout(
        """Submit a review when you get hired (within the year)
        to maintain access. You won't be required to submit a
        report right now.
        """,
        icon="info",
        width="100%",
    )


def callout_error() -> rx.Component:
    return rx.flex(
        rx.cond(
            OnboardState.onboard_has_error,
            rx.callout(
                OnboardState.onboard_error_message,
                width="100%",
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
            ),
        ),
        width="100%",
    )
