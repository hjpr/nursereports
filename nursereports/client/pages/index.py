
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
        rx.theme_panel(default_open=False),
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center bg-gradient-to-b from-white to-teal-200 min-h-svh"
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        header_image(),
        sponsors(),
        info_header(),
        info_cards(),
        class_name="flex-col items-center w-full"
    )


def header() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(
                """Hospital reviews for nurses, by nurses.""",
                class_name="font-bold text-center md:text-6xl text-4xl text-zinc-700"
            ),
            rx.text(
                """
                Find all the information you'll ever need on hospitals
                across the US. Share information on pay, benefits, unit
                culture, and staffing ratios.
                """,
                class_name="text-center text-zinc-700"
            ),
            rx.flex(
                rx.button(
                    "Get Started",
                    rx.icon("chevron-right"),
                    size="4",
                    on_click=rx.redirect("/create-account"),
                    class_name="bg-teal-600 w-full md:w-auto"
                ),
                rx.button(
                    "Learn More",
                    rx.icon("chevron-right"),
                    size="4",
                    on_click=rx.redirect("https://blog.nursereports.org/about-us"),
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 w-full md:w-auto cursor-pointer"
                ),
                class_name="flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4 w-full"
            ),
            class_name="flex-col space-y-10 w-full md:max-w-screen-sm"
        ),
        class_name="flex-col items-center px-4 py-24 w-full"
    )


def header_image() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.image(
                src="",
                class_name="rounded-lg h-auto w-auto"
            ),
            class_name="flex items-center justify-center border rounded-lg bg-white shadow-lg aspect-video justify-center h-full w-full"
        ),
        class_name="flex p-4 w-full max-w-screen-lg"
    )


def sponsors() -> rx.Component:
    return rx.flex(
        rx.text(
            """
            Are you looking to sponsor grassroots nursing
            empowerment?
            """,
            class_name="text-center text-zinc-700"
        ),
        rx.button(
            "Contact Us",
            size="3",
            variant="outline",
            on_click=rx.redirect("/contact-us")
        ),
        class_name="flex-col items-center justify-center px-4 py-24 space-y-6 w-full max-w-screen-sm"
    )


def info_header() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("messages-square", class_name="stroke-teal-700 h-10 w-10"),
            rx.flex(
                rx.text(
                    "Read unfiltered and anonymous reviews from everywhere",
                    class_name="text-2xl font-bold text-zinc-700 text-center"
                ),
                rx.text(
                    """
                    No more guessing about your current or future assignments.
                    Smartly summarized data built for career progression, and
                    workplace transparency.
                    """,
                    class_name="text-center text-zinc-700"
                ),
                class_name="flex-col items-center justify-center space-y-4 w-full"
            ),
            class_name="flex-col items-center justify-center space-y-10 w-full max-w-screen-sm"
        ),
        class_name="flex-col items-center bg-white px-4 py-24 w-full"
    )


def info_cards() -> rx.Component:
    return rx.flex(
        info_cards_top(),
        info_cards_bottom(),
        flex_direction="column",
        width="100%",
        gap="8px",
        bg="white",
    )


def info_cards_top() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.card(
                                rx.flex(
                                    rx.text("PLACEHOLDER", font_size="10px"),
                                    width="100%",
                                    height="100%",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                height="100%",
                                width="100%",
                                aspect_ratio="16 / 9",
                            ),
                            rx.text("Pay and Benefits", text_align="center"),
                            rx.text(
                                """
                                Know what you'll make, and compare
                                compensation between hospitals.
                                """,
                                font_size="13px",
                                text_align="center",
                                color="grey",
                            ),
                            flex_direction="column",
                            width="100%",
                            gap="8px",
                            padding="8px",
                        ),
                        flex_direction="column",
                        width="100%",
                    ),
                    bg="rgb(249 250 251)",
                    width="100%",
                    border_radius=[
                        "12px",
                        "48px 12px 12px 12px",
                        "48px 12px 12px 12px",
                        "48px 12px 12px 12px",
                        "48px 12px 12px 12px",
                    ],
                    padding="24px",
                ),
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.card(
                                rx.flex(
                                    rx.text("PLACEHOLDER", font_size="10px"),
                                    width="100%",
                                    height="100%",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                height="100%",
                                width="100%",
                                aspect_ratio="16 / 9",
                            ),
                            rx.text("Culture", text_align="center"),
                            rx.text(
                                """
                                Gone are the days of having to dig
                                up the inside scoop across social
                                media.
                                """,
                                font_size="13px",
                                text_align="center",
                                color="grey",
                            ),
                            flex_direction="column",
                            width="100%",
                            gap="8px",
                            padding="8px",
                        ),
                        flex_direction="column",
                        width="100%",
                    ),
                    bg="rgb(249 250 251)",
                    width="100%",
                    border_radius=[
                        "12px",
                        "12px 48px 12px 12px",
                        "12px 48px 12px 12px",
                        "12px 48px 12px 12px",
                        "12px 48px 12px 12px",
                    ],
                    padding="24px",
                ),
                flex_direction=["column", "row", "row", "row", "row"],
                width="100%",
                max_width="900px",
                gap="8px",
                padding_x=["24px", "24px", "0px", "0px", "0px"],
            ),
            flex_direction="column",
            width="100%",
            align_items="center",
        ),
        flex_direction="column",
        bg="white",
        align_items="center",
        width="100%",
    )


def info_cards_bottom() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.card(
                                rx.flex(
                                    rx.text("PLACEHOLDER", font_size="10px"),
                                    width="100%",
                                    height="100%",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                height="100%",
                                width="100%",
                                aspect_ratio="16 / 9",
                            ),
                            rx.text("Ratios", text_align="center"),
                            rx.text(
                                """
                                Find out about unit ratios, and get a
                                sense for workloads in each area.
                                """,
                                font_size="13px",
                                text_align="center",
                                color="grey",
                            ),
                            flex_direction="column",
                            width="100%",
                            gap="8px",
                            padding="8px",
                        ),
                        flex_direction="column",
                        width="100%",
                    ),
                    bg="rgb(249 250 251)",
                    width="100%",
                    border_radius=[
                        "12px",
                        "12px 12px 12px 48px",
                        "12px 12px 12px 48px",
                        "12px 12px 12px 48px",
                        "12px 12px 12px 48px",
                    ],
                    padding="24px",
                ),
                rx.flex(
                    rx.flex(
                        rx.flex(
                            rx.card(
                                rx.flex(
                                    rx.text("PLACEHOLDER", font_size="10px"),
                                    width="100%",
                                    height="100%",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                height="100%",
                                width="100%",
                                aspect_ratio="16 / 9",
                            ),
                            rx.text("Rankings", text_align="center"),
                            rx.text(
                                """
                                Analyze pay and workplace ratings by
                                hospital, or take a wider view and 
                                explore rankings by state.
                                """,
                                font_size="13px",
                                text_align="center",
                                color="grey",
                            ),
                            flex_direction="column",
                            width="100%",
                            gap="8px",
                            padding="8px",
                        ),
                        flex_direction="column",
                        width="100%",
                    ),
                    bg="rgb(249 250 251)",
                    width="100%",
                    border_radius=[
                        "12px",
                        "12px 12px 48px 12px",
                        "12px 12px 48px 12px",
                        "12px 12px 48px 12px",
                        "12px 12px 48px 12px",
                    ],
                    padding="24px",
                ),
                flex_direction=["column", "row", "row", "row", "row"],
                width="100%",
                max_width="900px",
                gap="8px",
                padding_x=["24px", "24px", "0px", "0px", "0px"],
            ),
            flex_direction="column",
            width="100%",
            align_items="center",
        ),
        flex_direction="column",
        bg="white",
        align_items="center",
        width="100%",
    )
