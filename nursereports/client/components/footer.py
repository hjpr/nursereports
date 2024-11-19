
from ...states import BaseState, NavbarState, UserState

import reflex as rx


def footer() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image(src="/vector/square-activity.svg", class_name="h-7 w-7 mb-1"),
                        rx.text(
                            "Nurse", 
                            on_click=rx.redirect("/"),
                            class_name="text-2xl cursor-pointer text-teal-700 pb-1 font-bold"
                        ),
                        rx.text(
                            "Reports", 
                            on_click=rx.redirect("/"),
                            class_name="text-2xl cursor-pointer text-zinc-700 pb-1 font-bold"
                        ),
                        class_name="flex-row items-center w-full",
                    ),
                    rx.flex(
                        rx.icon("instagram", color="grey", cursor="pointer"),
                        rx.icon("facebook", color="grey", cursor="pointer"),
                        rx.icon("linkedin", color="grey", cursor="pointer"),
                        class_name="flex-row space-x-14"
                    ),
                    class_name="flex-col justify-between mb-16 w-full min-h-24 md:min-h-32"
                ),
                rx.flex(
                    rx.flex(
                        rx.link(
                            "Staff",
                            href=f"{BaseState.host_address}/for-staff",
                            size="2",
                            cursor="pointer",
                        ),
                        rx.link(
                            "Travelers",
                            href=f"{BaseState.host_address}/for-travelers",
                            size="2",
                            cursor="pointer",
                        ),
                        rx.link(
                            "Students",
                            href=f"{BaseState.host_address}/for-students",
                            size="2",
                            cursor="pointer",
                        ),
                        rx.link(
                            "Donate",
                            href=f"{BaseState.host_address}/donate",
                            size="2",
                            cursor="pointer"
                        ),
                        class_name="flex-col space-y-4 w-full"
                    ),
                    rx.flex(
                        rx.link(
                            "About Us",
                            href=f"{BaseState.host_address}/about-us",
                            size="2",
                            cursor="pointer"
                        ),
                        rx.cond(
                            UserState.user_claims_authenticated,
                            rx.link(
                                "Feedback",
                                size="2",
                                cursor="pointer",
                                on_click=NavbarState.set_show_feedback(True)
                            ),
                        ),
                        rx.link(
                            "Contact Us",
                            href=f"{BaseState.host_address}/contact-us",
                            size="2",
                            cursor="pointer"
                            ),
                        rx.link(
                            "Roadmap",
                            href=f"{BaseState.host_address}/roadmap",
                            size="2",
                            cursor="pointer"
                        ),
                        class_name="flex-col space-y-4 w-full"
                    ),
                    class_name="flex-row w-full"
                ),
                class_name="flex-col md:flex-row p-8 w-full min-h-32"
            ),
            rx.flex(
                rx.flex(
                    rx.icon("copyright", class_name="h-4 w-4"),
                    rx.text("2024 Nurse Reports", class_name="text-sm pl-4"),
                    class_name="flex-row items-center text-zinc-400"
                ),
                class_name="flex-col items-center w-full"
            ),
            class_name="flex-col space-y-8 w-full max-w-screen-md"
        ),
        class_name="flex-col bg-white items-center justify-center py-32 w-full"
    )