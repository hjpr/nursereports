from ..components import (
    solid_button,
    outline_button,
    text,
    flex,
    footer,
    navbar,
)
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/",
    title="Nurse Reports",
    on_load=BaseState.event_state_handle_sso_redirect
)
def index_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center dark:bg-zinc-900 w-full min-h-screen",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        header_image(),
        sponsors(),
        info_header(),
        info_cards(),
        class_name="flex-col items-center w-full",
    )


def header() -> rx.Component:
    return rx.flex(
        rx.flex(
            text(
                """Hospital reviews for nurses, by nurses.""",
                class_name="font-bold text-center md:text-6xl text-4xl dark:text-teal-600",
            ),
            text(
                """
                Find all the information you'll ever need on hospitals
                across the US. Share information on pay, benefits, unit
                culture, and staffing ratios.
                """,
                class_name="text-center",
            ),
            rx.flex(
                solid_button(
                    "Get Started",
                    rx.icon("chevron-right"),
                    size="4",
                    on_click=rx.redirect("/create-account"),
                ),
                outline_button(
                    "Learn More",
                    rx.icon("chevron-right"),
                    size="4",
                    on_click=rx.redirect("/about-us"),
                ),
                class_name="flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4 w-full",
            ),
            class_name="flex-col space-y-10 w-full md:max-w-screen-sm",
        ),
        class_name="flex-col items-center px-4 py-24 w-full",
    )


def header_image() -> rx.Component:
    return rx.flex(
        flex(
            text("PLACEHOLDER", class_name="text-xs"),
            class_name="items-center justify-center bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-500 rounded-lg shadow-lg aspect-square md:aspect-video justify-center h-full w-full",
        ),
        class_name="flex p-4 w-full max-w-screen-lg",
    )


def sponsors() -> rx.Component:
    return rx.flex(
        text(
            """
            Are you looking to sponsor grassroots nursing
            empowerment?
            """,
            class_name="text-center",
        ),
        outline_button(
            "Contact Us",
            rx.icon("chevron-right"),
            size="4",
            on_click=rx.redirect("/contact-us"),
        ),
        class_name="flex-col items-center justify-center px-4 py-24 space-y-8 w-full max-w-screen-sm",
    )


def info_header() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("messages-square", class_name="stroke-teal-700 h-10 w-10"),
            rx.flex(
                text(
                    "Read unfiltered and anonymous reviews from everywhere.",
                    class_name="text-2xl font-bold text-center",
                ),
                text(
                    """
                    No more guessing about your current or future assignments.
                    Smartly summarized data built for career progression, and
                    workplace transparency.
                    """,
                    class_name="text-center",
                ),
                class_name="flex-col items-center justify-center space-y-4 w-full",
            ),
            class_name="flex-col items-center justify-center space-y-10 w-full max-w-screen-sm",
        ),
        class_name="flex-col items-center px-4 py-24 w-full",
    )


def info_cards() -> rx.Component:
    return rx.flex(info_cards_top(), info_cards_bottom(), class_name="flex-col w-full")


def info_cards_top() -> rx.Component:
    return rx.flex(
        rx.flex(
            flex(
                flex(
                    flex(
                        rx.flex(
                            text("PLACEHOLDER", class_name="text-xs"),
                            class_name="flex-col bg-white dark:bg-zinc-800 items-center justify-center h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    text("Pay and Benefits", class_name="text-lg font-bold"),
                    text(
                        """
                        Know what you'll make, and compare
                        compensation between hospitals.
                        """,
                        class_name="text-sm text-center",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border border-zinc-200 dark:border-zinc-500 rounded-lg rounded-t-[48px] md:rounded-tr-lg p-6 w-full",
            ),
            flex(
                flex(
                    flex(
                        rx.flex(
                            text("PLACEHOLDER", class_name="text-xs"),
                            class_name="flex-col bg-white dark:bg-zinc-800 items-center justify-center h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    text("Culture", class_name="text-lg font-bold"),
                    text(
                        """
                        Gone are the days of having to dig
                        up the inside scoop across social
                        media.
                        """,
                        class_name="text-sm text-center",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border border-zinc-200 dark:border-zinc-500 rounded-lg md:rounded-tr-[48px] p-6 w-full",
            ),
            class_name="flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 w-full max-w-screen-lg",
        ),
        class_name="flex-col items-center px-4 py-2 w-full",
    )


def info_cards_bottom() -> rx.Component:
    return rx.flex(
        rx.flex(
            flex(
                flex(
                    flex(
                        rx.flex(
                            text("PLACEHOLDER", class_name="text-xs"),
                            class_name="flex-col bg-white dark:bg-zinc-800 items-center justify-center h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    text("Ratios", class_name="text-lg font-bold"),
                    text(
                        """
                        Find out about unit ratios, and get a
                        sense for workloads in each area.
                        """,
                        class_name="text-sm text-center",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border border-zinc-200 dark:border-zinc-500 rounded-lg md:rounded-bl-[48px] p-6 w-full",
            ),
            flex(
                flex(
                    flex(
                        rx.flex(
                            text("PLACEHOLDER", class_name="text-xs"),
                            class_name="flex-col bg-white dark:bg-zinc-800 items-center justify-center h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    text("Rankings", class_name="text-lg font-bold"),
                    text(
                        """
                        Analyze pay and workplace ratings by
                        hospital, or take a wider view and 
                        explore rankings by state.
                        """,
                        class_name="text-sm text-center",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border border-zinc-200 dark:border-zinc-500 rounded-lg rounded-b-[48px] md:rounded-br-[48px] md:rounded-bl-lg p-6 w-full",
            ),
            class_name="flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 w-full max-w-screen-lg",
        ),
        class_name="flex-col items-center px-4 py-2 pb-20 w-full",
    )
