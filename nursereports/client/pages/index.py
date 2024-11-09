from ..components.custom import spacer
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base_state import BaseState
from ...states.login_state import LoginState

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
        background="linear-gradient(ghostwhite, honeydew)",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        spacer(height="36px"),
        header_image(),
        spacer(height="48px"),
        sponsors(),
        spacer(height="24px"),
        info_header(),
        info_cards(),
        width="100%",
        align="center",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )


def header() -> rx.Component:
    return rx.center(
        rx.flex(
            spacer(height="56px"),
            rx.text(
                """Hospital reviews for nurses, by nurses.""",
                font_size=["36px", "36px", "56px", "56px", "56px"],
                font_weight="bold",
                line_height=["1.1", "1.1", "1.2", "1.2", "1.2"],
                color_scheme="teal",
                text_align="center",
            ),
            rx.text(
                """
                Find all the information you'll ever need on hospitals
                across the US. Share information on pay, benefits, unit
                culture, and staffing ratios.
                """,
                text_align="center",
                line_height=["1.5", "1.5", "2", "2", "2"],
                color_scheme="gray",
            ),
            rx.flex(
                rx.button(
                    "Get Started",
                    rx.icon("chevron-right"),
                    on_click=[
                        LoginState.set_current_tab("create_account"),
                        rx.redirect("/login")
                    ],
                    width=["100%", "100%", "auto", "auto", "auto"],
                    radius="full",
                    color_scheme="teal",
                    size="4",
                    border="4px solid gainsboro",
                ),
                rx.button(
                    "Learn More",
                    rx.icon("chevron-right"),
                    on_click=rx.redirect("https://blog.nursereports.org/about-us"),
                    width=["100%", "100%", "auto", "auto", "auto"],
                    radius="full",
                    color_scheme="teal",
                    variant="ghost",
                    size="4",
                ),
                flex_direction=["column", "column", "row", "row", "row"],
                width="100%",
                gap=["20px", "20px", "36px", "36px", "36px"],
                align_items="center",
                justify_content="center",
                margin="8px 0px 0px 0px",
                padding="0 48px 0 48px",
            ),
            flex_direction="column",
            gap="24px",
            max_width=["480px", "480px", "640px", "640px", "640px"],
            padding="0px 12px",
        ),
        padding="24px",
        width="100%",
    )


def header_image() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.flex(
                rx.text("PLACEHOLDER", font_size="10px"),
                height="100%",
                width="100%",
                align_items="center",
                justify_content="center",
            ),
            width="100%",
            border="10px solid whitesmoke",
        ),
        width="100%",
        max_width="1100px",
        padding_x="24px",
        aspect_ratio="16 / 9",
    )


def sponsors() -> rx.Component:
    return rx.flex(
        spacer(),
        rx.text(
            """
            Are you looking to sponsor grassroots nursing
            empowerment?
            """,
            text_align="center",
            line_height=["1.5", "1.5", "2", "2", "2"],
            color_scheme="gray",
        ),
        rx.button("Contact Us", size="4", radius="full", variant="soft"),
        spacer(),
        flex_direction="column",
        width="100%",
        max_width="640px",
        gap="48px",
        align_items="center",
        justify_content="center",
        padding="0 48px 0 48px",
    )


def info_header() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("messages-square", size=36, color="grey"),
            rx.text(
                """
                No more guessing about your current or future
                assignments.
                """,
                font_size=["32px", "32px", "36px", "36px", "36px"],
                font_weight="bold",
                line_height=["1.1", "1.1", "1.2", "1.2", "1.2"],
                color_scheme="teal",
                text_align="center",
            ),
            rx.text(
                "Read unfiltered and anonymous reviews from everywhere.",
                text_align="center",
                color="grey",
            ),
            flex_direction="column",
            width="100%",
            gap="24px",
            align_items="center",
            justify_content="center",
            max_width="768px",
        ),
        bg="white",
        width="100%",
        justify_content="center",
        padding="128px 48px 64px 48px",
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
