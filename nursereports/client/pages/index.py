from ..components.footer import footer
from ..components.navbar import navbar
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/",
    title="Nurse Reports",
    on_load=BaseState.event_state_auth_flow,
)
def index_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-gradient-to-b from-white to-teal-200 w-full min-h-svh",
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
            rx.text(
                """Hospital reviews for nurses, by nurses.""",
                class_name="font-bold text-center md:text-6xl text-4xl text-zinc-700",
            ),
            rx.text(
                """
                Find all the information you'll ever need on hospitals
                across the US. Share information on pay, benefits, unit
                culture, and staffing ratios.
                """,
                class_name="text-center text-zinc-700",
            ),
            rx.flex(
                rx.button(
                    "Get Started",
                    rx.icon("chevron-right"),
                    size="4",
                    on_click=rx.redirect("/create-account"),
                    class_name="bg-teal-600 w-full md:w-auto cursor-pointer",
                ),
                rx.button(
                    "Learn More",
                    rx.icon("chevron-right"),
                    size="4",
                    on_click=rx.redirect("/about-us"),
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 w-full md:w-auto cursor-pointer",
                ),
                class_name="flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4 w-full",
            ),
            class_name="flex-col space-y-10 w-full md:max-w-screen-sm",
        ),
        class_name="flex-col items-center px-4 py-24 w-full",
    )


def header_image() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.image(src="", class_name="rounded-lg h-auto w-auto"),
            class_name="flex items-center justify-center border rounded-lg bg-white shadow-lg aspect-square md:aspect-video justify-center h-full w-full",
        ),
        class_name="flex p-4 w-full max-w-screen-lg",
    )


def sponsors() -> rx.Component:
    return rx.flex(
        rx.text(
            """
            Are you looking to sponsor grassroots nursing
            empowerment?
            """,
            class_name="text-center text-zinc-700",
        ),
        rx.button(
            "Contact Us",
            rx.icon("chevron-right"),
            size="4",
            on_click=rx.redirect("/contact-us"),
            class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 cursor-pointer",
        ),
        class_name="flex-col items-center justify-center px-4 py-24 space-y-8 w-full max-w-screen-sm",
    )


def info_header() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("messages-square", class_name="stroke-teal-700 h-10 w-10"),
            rx.flex(
                rx.text(
                    "Read unfiltered and anonymous reviews from everywhere.",
                    class_name="text-2xl font-bold text-zinc-700 text-center",
                ),
                rx.text(
                    """
                    No more guessing about your current or future assignments.
                    Smartly summarized data built for career progression, and
                    workplace transparency.
                    """,
                    class_name="text-center text-zinc-700",
                ),
                class_name="flex-col items-center justify-center space-y-4 w-full",
            ),
            class_name="flex-col items-center justify-center space-y-10 w-full max-w-screen-sm",
        ),
        class_name="flex-col items-center bg-white px-4 py-24 w-full",
    )


def info_cards() -> rx.Component:
    return rx.flex(
        info_cards_top(), info_cards_bottom(), class_name="flex-col bg-white w-full"
    )


def info_cards_top() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.text("PLACEHOLDER", font_size="10px"),
                            class_name="flex-col items-center justify-center bg-white h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    rx.text(
                        "Pay and Benefits", class_name="text-lg font-bold text-zinc-700"
                    ),
                    rx.text(
                        """
                        Know what you'll make, and compare
                        compensation between hospitals.
                        """,
                        class_name="text-sm text-center text-zinc-700",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border rounded-lg rounded-t-[48px] md:rounded-tr-lg bg-zinc-50 p-6 w-full",
            ),
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.text("PLACEHOLDER", font_size="10px"),
                            class_name="flex-col items-center justify-center bg-white h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    rx.text("Culture", class_name="text-lg font-bold text-zinc-700"),
                    rx.text(
                        """
                        Gone are the days of having to dig
                        up the inside scoop across social
                        media.
                        """,
                        class_name="text-sm text-center text-zinc-700",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border rounded-lg md:rounded-tr-[48px] bg-zinc-50 p-6 w-full",
            ),
            class_name="flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 w-full max-w-screen-lg",
        ),
        class_name="flex-col items-center px-4 py-2 w-full",
    )


def info_cards_bottom() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.text("PLACEHOLDER", font_size="10px"),
                            class_name="flex-col items-center justify-center bg-white h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    rx.text("Ratios", class_name="text-lg font-bold text-zinc-700"),
                    rx.text(
                        """
                        Find out about unit ratios, and get a
                        sense for workloads in each area.
                        """,
                        class_name="text-sm text-center text-zinc-700",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border rounded-lg md:rounded-bl-[48px] bg-zinc-50 p-6 w-full",
            ),
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.text("PLACEHOLDER", font_size="10px"),
                            class_name="flex-col items-center justify-center bg-white h-full w-full",
                        ),
                        class_name="rounded aspect-video h-full w-full",
                    ),
                    rx.text("Rankings", class_name="text-lg font-bold text-zinc-700"),
                    rx.text(
                        """
                        Analyze pay and workplace ratings by
                        hospital, or take a wider view and 
                        explore rankings by state.
                        """,
                        class_name="text-sm text-center text-zinc-700",
                    ),
                    class_name="flex-col items-center p-4 space-y-4 w-full",
                ),
                class_name="flex-col border rounded-lg rounded-b-[48px] md:rounded-br-[48px] md:rounded-bl-lg bg-zinc-50 p-6 w-full",
            ),
            class_name="flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 w-full max-w-screen-lg",
        ),
        class_name="flex-col items-center px-4 py-2 w-full",
    )
