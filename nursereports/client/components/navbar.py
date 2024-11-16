
from ...states import (
    BaseState,
    NavbarState
)

import reflex as rx

def navbar() -> rx.Component:
    return rx.flex(
        feedback(),
            rx.flex(
                logo(),
                links(),
                rx.spacer(),
                rx.flex(
                    search(),
                    login_or_account(),
                    mobile_menu(),
                    class_name="flex-row space-x-2"
                ),
                class_name="flex-row items-center justify-between p-4 w-full max-w-screen-xl",
            ),
        class_name="flex-col border items-center justify-center sticky top-0 z-10 bg-white border-b-zinc-300 h-16 w-full"
    )

def feedback() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Provide feedback."),
            rx.form(
                rx.dialog.description(
                    rx.text_area(
                        name="feedback",
                        placeholder="Suggestions, improvements, or kudos?",
                        height="150px",
                        max_length=500,
                    )
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            type="button",
                            variant="soft",
                            size="3",
                            radius="full",
                            on_click=NavbarState.set_show_feedback(False),
                        )
                    ),
                    rx.dialog.close(
                        rx.button("Submit", type="submit", size="3", radius="full")
                    ),
                    spacing="3",
                    justify="end",
                ),
                on_submit=NavbarState.event_state_submit_feedback,
            ),
        ),
        open=NavbarState.show_feedback,
    )


def logo() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.image(
                src="/vector/square-activity.svg",
                class_name="h-9 md:h-7 w-9 md:w-7"
            ),
            rx.flex(
                rx.text(
                    "Nurse",
                    on_click=rx.redirect("/"),
                    class_name="hidden md:flex text-2xl font-bold text-teal-700 cursor-pointer"
                ),
                rx.text(
                    "N",
                    class_name="flex md:hidden text-3xl font-bold text-teal-700 cursor-pointer"
                ),
                rx.text(
                    "Reports",
                    on_click=rx.redirect("/"),
                    class_name="hidden md:flex text-2xl font-bold text-zinc-700 cursor-pointer"
                ),
                rx.text(
                    "R",
                    on_click=rx.redirect("/"),
                    class_name="flex md:hidden text-3xl font-bold text-zinc-700 cursor-pointer"
                )
            ),
            class_name="flex-row items-center"
        ),
        class_name="flex-row items-center space-x-8 justify-center"
    )


def links() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,
        
        # Nothing displayed if user is authenticated.
        rx.flex(),

        # Links displayed if user not authenticated.
        rx.flex(
            rx.link(
                "Staff",
                href=f"{BaseState.host_address}/for-staff",
                class_name="cursor-pointer text-zinc-700"
            ),
            rx.link(
                "Travelers",
                href=f"{BaseState.host_address}/for-travelers",
                class_name="cursor-pointer text-zinc-700"
            ),
            rx.link(
                "Students",
                href=f"{BaseState.host_address}/for-students",
                class_name="cursor-pointer text-zinc-700"
            ),
            rx.flex(
                rx.link(
                    "Donate",
                    href=f"{BaseState.host_address}/donate",
                    class_name="cursor-pointer text-teal-700"
                ),
                class_name="flex-row items-center space-x-2 cursor-pointer"
            ),
            class_name="flex-row space-x-8 hidden md:flex ml-8"
        )
    )

def search() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,

        # Shows search if user is logged in
        rx.flex(
            rx.button(
                rx.icon("search", class_name="h-5 w-5"),
                rx.text("Search", class_name="hidden md:flex"),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg cursor-pointer",
                on_click=rx.redirect("/search/hospital")
            )
        ),

        # Hides search if user not logged in.
        rx.flex()
    )

def login_or_account() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,

        # Show account if user is logged in.
        rx.flex(
            rx.button(
                rx.icon("circle-user-round", class_name="h-5 w-5"),
                on_click=rx.redirect("/my-account"),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg cursor-pointer",
            ),
        ),

        # Show login if user not logged in.
        rx.flex(
            rx.button(
                "Login",
                on_click=rx.redirect("/login"),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg cursor-pointer",
            ),
        )
    )

def mobile_menu() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,

        # Show mobile menu for logged in users.
        rx.cond(
            BaseState.user_has_reported,

            # Show menu for logged in and onboarded users.
            rx.flex(
                rx.drawer.root(
                    rx.drawer.trigger(
                        rx.button(
                            rx.icon("menu", class_name="h-5 w-5"),
                            class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg"
                        )
                    ),
                    rx.drawer.overlay(),
                    rx.drawer.portal(
                        rx.drawer.content(
                            rx.flex(
                                rx.flex(
                                    rx.heading("NurseReports"),
                                    rx.spacer(),
                                    rx.drawer.close(rx.icon("X", cursor="pointer")),
                                    class_name="flex-row justify-center p-8 w-full"
                                ),
                                rx.flex(
                                    rx.link(
                                        "Hospital Search",
                                        href=f"{BaseState.host_address}/search/hospital",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                rx.flex(
                                    rx.link(
                                        "State Summary",
                                        href=f"{BaseState.host_address}/search/state",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                rx.flex(
                                    rx.link(
                                        "Dashboard",
                                        href=f"{BaseState.host_address}/dashboard",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                rx.flex(
                                    rx.link(
                                        "Donate",
                                        href=f"{BaseState.host_address}/donate",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                rx.flex(
                                    rx.flex(
                                        rx.link(
                                            "Logout",
                                            class_name="text-zinc-700 cursor-pointer",
                                            on_click=BaseState.event_state_logout
                                        ),
                                        rx.icon("log-out", class_name="h-5 w-5 text-zinc-700"),
                                        class_name="flex-row items-center space-x-4"
                                    ),
                                    class_name="flex-row p-8 w-full"
                                ),
                                class_name="flex-col divide-y w-full"
                            ),
                            class_name="h-full w-full bg-white"
                        )
                    ),
                    direction="top",
                ),
                class_name="flex md:hidden cursor-pointer"
            ),

            # Show menu for logged in but not onboarded users.
            rx.flex(
                rx.drawer.root(
                    rx.drawer.trigger(
                        rx.button(
                            rx.icon("menu", class_name="h-5 w-5"),
                            class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg"
                        )
                    ),
                    rx.drawer.overlay(),
                    rx.drawer.portal(
                        rx.drawer.content(
                            rx.flex(
                                rx.flex(
                                    rx.heading("NurseReports"),
                                    rx.spacer(),
                                    rx.drawer.close(rx.icon("X", cursor="pointer")),
                                    class_name="flex-row justify-center p-8 w-full"
                                ),
                                rx.flex(
                                    rx.flex(
                                        rx.link(
                                            "Logout",
                                            class_name="text-zinc-700 cursor-pointer",
                                            on_click=BaseState.event_state_logout
                                        ),
                                        rx.icon("log-out", class_name="text-zinc-700"),
                                        class_name="space-x-4"
                                    ),
                                    class_name="flex-row p-8 w-full"
                                ),
                                class_name="flex-col divide-y bg-white"
                            )
                        )
                    ),
                    direction="top"
                ),
                class_name="flex md:hidden cursor-pointer",
            )
        ),

        # Show menu for users not logged in.
        rx.flex(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.button(
                        rx.icon("menu", class_name="h-5 w-5"),
                        class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg focus:outline-none"
                    )
                ),
                rx.drawer.overlay(),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.flex(
                            rx.flex(
                                rx.heading("NurseReports"),
                                rx.spacer(),
                                rx.drawer.close(rx.icon("X", cursor="pointer")),
                                class_name="flex-row justify-center p-8 w-full"
                            ),
                            rx.flex(
                                rx.link(
                                    "Staff",
                                    href=f"{BaseState.host_address}/for-staff",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            rx.flex(
                                rx.link(
                                    "Travelers",
                                    href=f"{BaseState.host_address}/for-travelers",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            rx.flex(
                                rx.link(
                                    "Students",
                                    href=f"{BaseState.host_address}/for-students",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            rx.flex(
                                rx.link(
                                    "Donate",
                                    href=f"{BaseState.host_address}/donate",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            rx.flex(
                                rx.flex(
                                    rx.link(
                                        "Login",
                                        on_click=rx.redirect("/login"),
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    rx.icon("log-in", class_name="h-5 w-5 text-zinc-700"),
                                    class_name="flex-row items-center space-x-4"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            class_name="flex-col divide-y w-full"
                        ),
                        class_name="h-full w-full bg-white"
                    )
                ),
                direction="top",
            ),
            class_name="flex md:hidden cursor-pointer"
        )
    )