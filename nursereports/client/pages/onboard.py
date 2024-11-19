from ..components.c2a import c2a
from ..components.custom import login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states import BaseState, OnboardState, SearchState

import reflex as rx


@rx.page(
    route="/onboard",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_auth_flow,
        BaseState.event_state_access_flow("login"),
    ],
)
@login_protected
def onboard_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-gradient-to-b from-white to-teal-200 min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(
        greeting(),
        questions(),
        button(),
        class_name="flex-col items-center space-y-10 px-4 py-24 w-full md:max-w-screen-sm",
    )


def greeting() -> rx.Component:
    return rx.flex(
        rx.text(
            """Welcome to the community!""",
            class_name="font-bold text-center md:text-6xl text-4xl text-zinc-700",
        ),
        rx.flex(
            rx.text(
                """
                Hey! I'm Jeremy. I'm an ICU nurse still working bedside
                on the East Coast. I built this tool to help nurses
                share hospital information across the US.
                """,
                class_name="text-center text-zinc-700",
            ),
            rx.text(
                """
                This community will always be free to access, I simply
                ask that you share a report first if you are currently
                working in a hospital.
                """,
                class_name="text-center text-zinc-700",
            ),
            class_name="flex-col items-center space-y-6 w-full",
        ),
        class_name="flex-col space-y-10 pb-4 w-full max-w-screen-sm",
    )


def questions() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text("Onboarding Questions", class_name="text-xl font-bold"),
                rx.divider(),
                class_name="flex-col space-y-2 w-full",
            ),
            rx.flex(
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
                    width="100%",
                ),
                class_name="flex-col space-y-1 w-full",
            ),
            rx.cond(
                OnboardState.license,
                rx.cond(
                    ~OnboardState.is_student,
                    rx.flex(
                        rx.flex(
                            rx.text("What state are you licensed in?"),
                            rx.select(
                                SearchState.state_options,
                                placeholder="- Select one -",
                                value=OnboardState.license_state,
                                on_change=OnboardState.set_license_state,
                                required=True,
                                size="3",
                                width="100%",
                            ),
                            class_name="flex-col space-y-1 w-full",
                        ),
                        rx.flex(
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
                                width="100%",
                            ),
                            class_name="flex-col space-y-1 w-full",
                        ),
                        class_name="flex-col space-y-4 w-full",
                    ),
                ),
            ),
            rx.cond(~OnboardState.can_give_review, callout_review()),
            callout_error(),
            class_name="flex-col space-y-4 w-full",
        ),
        class_name="flex-col border rounded-lg bg-white p-4 w-full",
    )


def button() -> rx.Component:
    return rx.flex(
        rx.button(
            "Let's go!",
            rx.icon("chevron-right"),
            size="4",
            on_click=OnboardState.event_state_submit_onboard,
        ),
        width="100%",
        justify_content="center",
    )


def callout_review() -> rx.Component:
    return rx.flex(
        rx.callout(
            """Submit a review when you get hired (within the year)
            to maintain access. You won't be required to submit a
            report right now.
            """,
            icon="info",
            class_name="text-zinc-700 w-full",
        ),
        class_name="pt-2 w-full",
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
