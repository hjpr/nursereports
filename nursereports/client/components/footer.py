from .custom import spacer

import reflex as rx


def footer() -> rx.Component:
    return rx.flex(
        spacer(height="120px"),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image(
                            src="/vector/square-activity.svg",
                            height="22px",
                            width="22px",
                            margin="4px 0 0 0",
                        ),
                        rx.heading("Nurse Reports", color="grey", padding="0 0 48px 0"),
                        flex_direction="row",
                        gap="6px",
                        justify_content="center",
                    ),
                    rx.flex(
                        rx.icon("instagram", color="grey", cursor="pointer"),
                        rx.divider(orientation="vertical"),
                        rx.icon("facebook", color="grey", cursor="pointer"),
                        rx.divider(orientation="vertical"),
                        rx.icon("linkedin", color="grey", cursor="pointer"),
                        flex_direction="row",
                        gap="20px",
                    ),
                    flex_direction="column",
                    width="100%",
                    align_items="start",
                    justify_content="space-between",
                    padding=[
                        "0 0 48px 0",
                        "0 0 48px 0",
                        "0 0 0 0",
                        "0 0 0 0",
                        "0 0 0 0",
                    ],
                ),
                rx.flex(
                    rx.flex(
                        rx.link(
                            "Students",
                            on_click=rx.redirect(
                                "https://blog.nursereports.org/for-students"
                            ),
                            size="2",
                        ),
                        rx.link(
                            "Staff",
                            on_click=rx.redirect(
                                "https://blog.nursereports.org/for-staff"
                            ),
                            size="2",
                        ),
                        rx.link(
                            "Travelers",
                            on_click=rx.redirect(
                                "https://blog.nursereports.org/for-travelers"
                            ),
                            size="2",
                        ),
                        rx.flex(
                            rx.link("Donate", size="2"),
                            rx.icon("sparkle", color="teal", size=14),
                            gap="8px",
                            align_items="center",
                        ),
                        flex_direction="column",
                        gap="12px",
                        width="100%",
                    ),
                    rx.flex(
                        rx.link(
                            "About Us",
                            on_click=rx.redirect(
                                "https://blog.nursereports.org/about-us"
                            ),
                            size="2",
                        ),
                        rx.link("Feedback", size="2"),
                        rx.link("Contact", size="2"),
                        rx.link(
                            "Roadmap",
                            on_click=rx.redirect(
                                "https://blog.nursereports.org/roadmap"
                            ),
                            size="2",
                        ),
                        flex_direction="column",
                        gap="12px",
                        width="100%",
                        padding="0 0 0 48px",
                    ),
                    flex_direction="row",
                    width="100%",
                ),
                flex_direction=["column", "column", "row", "row", "row"],
                width="100%",
            ),
            rx.divider(),
            rx.flex(
                rx.flex(
                    rx.icon("copyright", size=14, color="grey"),
                    rx.text("2024 Nurse Reports", size="2", color="grey"),
                    flex_direction="row",
                    gap="8px",
                    align_items="center",
                ),
                width="100%",
                justify_content="center",
            ),
            flex_direction="column",
            width="100%",
            max_width="768px",
            gap="64px",
            padding="0 36px 0 36px",
        ),
        spacer(height="100px"),
        bg="white",
        min_height="260px",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="0",
        flex_shrink="0",
        width="100%",
        justify_content="center",
        align_items="center",
    )
