from ..components import login_protected, flex, footer, navbar, text
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
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(
        greeting(),
        questions(),
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
    return flex(
        rx.flex(
            text("Nursing Information", class_name="text-2xl font-bold"),
            class_name="flex-col items-center bg-zinc-100 dark:bg-zinc-800 p-6 w-full",
        ),
        flex(
            rx.flex(
                rx.flex(
                    rx.text("What is your license?"),
                    rx.flex(
                        rx.cond(
                            OnboardState.license,
                            rx.icon("circle-check-big", class_name="stroke-green-400"),
                            rx.icon("circle-alert", class_name="stroke-zinc-200"),
                        ),
                        class_name="pl-4",
                    ),
                    class_name="flex-row justify-between w-full",
                ),
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
                    position="popper",
                    on_change=OnboardState.set_license,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            rx.flex(
                rx.flex(
                    rx.cond(
                        OnboardState.license == "Nursing Student",
                        rx.text("What state do you attend school in?"),
                        rx.text("What is the primary state in which you practice?"),
                    ),
                    rx.flex(
                        rx.cond(
                            OnboardState.license_state,
                            rx.icon(
                                "circle-check-big",
                                class_name="h-6 w-6 stroke-green-400",
                            ),
                            rx.icon(
                                "circle-alert", class_name="h-6 w-6 stroke-zinc-200"
                            ),
                        ),
                        class_name="pl-4",
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.select(
                    SearchState.state_options,
                    placeholder="- Select one -",
                    value=OnboardState.license_state,
                    position="popper",
                    on_change=OnboardState.set_license_state,
                    required=True,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            rx.flex(
                rx.flex(
                    rx.text(" Have you worked in a hospital in some nursing role within the past year? "),
                    rx.flex(
                        rx.cond(
                            (OnboardState.license == "Nursing Student") |
                            (OnboardState.has_review),
                            rx.icon(
                                "circle-check-big",
                                class_name="h-6 w-6 stroke-green-400",
                            ),
                            rx.icon(
                                "circle-alert", class_name="h-6 w-6 stroke-zinc-200"
                            ),
                        ),
                        class_name="pl-4",
                    ),
                    class_name="flex-row justify-between w-full",
                ),
                rx.select(
                    ["Yes", "No"],
                    placeholder="- Select one -",
                    value=OnboardState.has_review,
                    position="popper",
                    on_change=OnboardState.set_has_review,
                    required=True,
                    disabled=(OnboardState.license == "Nursing Student"),
                    size="3",
                    width="100%",
                ),
                class_name="flex-col space-y-2 p-4 w-full",
            ),
            rx.cond(
                (OnboardState.license
                == "Nursing Student") | (OnboardState.has_review
                == "No"),
                rx.flex(
                    rx.callout(
                        """
                        You won't be required to submit a
                        report right now.
                        """,
                        icon="info",
                        class_name="text-zinc-700 w-full",
                    ),
                    class_name="flex-col space-y-2 p-4 w-full",
                ),
            ),
            rx.flex(
                rx.flex(
                    rx.text("Next", class_name="font-bold select-none"),
                    rx.icon("arrow-right"),
                    on_click=OnboardState.event_state_submit_onboard,
                    class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer",
                ),
                class_name="flex-col w-full active:bg-zinc-200 transition-colors duration-75",
            ),
            class_name="flex-col dark:divide-zinc-500 space-y-2 divide-y w-full",
        ),
        class_name="flex-col border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )
