from .tailwind import (
    flex,
    link,
    outline_button
)

from ...states import (
    AuthState,
    BaseState,
    UserState,
    NavbarState
)

import reflex as rx

def navbar() -> rx.Component:
    return flex(
        feedback(),
        flex(
            logo(),
            links(),
            rx.spacer(),
            flex(
                search(),
                dashboard(),
                login_or_account(),
                mobile_menu(),
                class_name="flex-row space-x-2"
            ),
            class_name="flex-row items-center justify-between p-3 w-full max-w-screen-xl",
        ),
        class_name="flex-col border border-zinc-100 dark:border-zinc-900 border-b-zinc-200 dark:border-b-zinc-500 items-center justify-center sticky top-0 z-10 h-16 w-full"
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
                flex(
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
    return flex(
        flex(
            rx.image(
                src="/vector/square-activity.svg",
                class_name="h-9 md:h-7 w-9 md:w-7"
            ),
            flex(
                rx.text(
                    "Nurse",
                    on_click=rx.cond(
                        UserState.user_claims_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/")
                    ),
                    class_name="hidden md:flex text-2xl font-bold text-teal-700 dark:text-zinc-200 cursor-pointer"
                ),
                rx.text(
                    "N",
                    on_click=rx.cond(
                        UserState.user_claims_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/")
                    ),
                    class_name="flex md:hidden text-3xl font-bold text-teal-700 dark:text-zinc-200 cursor-pointer"
                ),
                rx.text(
                    "Reports",
                    on_click=rx.cond(
                        UserState.user_claims_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/")
                    ),
                    class_name="hidden md:flex text-2xl font-bold text-zinc-700m dark:text-zinc-200 cursor-pointer"
                ),
                rx.text(
                    "R",
                    on_click=rx.cond(
                        UserState.user_claims_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/")
                    ),
                    class_name="flex md:hidden text-3xl font-bold text-zinc-700 dark:text-zinc-200 cursor-pointer"
                )
            ),
            class_name="flex-row items-center"
        ),
        class_name="flex-row items-center space-x-8 justify-center"
    )


def links() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,
        
        # Nothing displayed if user is authenticated.
        flex(),

        # Links displayed if user not authenticated.
        flex(
            link(
                "Staff",
                href=f"{BaseState.host_address}/for-staff",
            ),
            link(
                "Travelers",
                href=f"{BaseState.host_address}/for-travelers",
            ),
            link(
                "Students",
                href=f"{BaseState.host_address}/for-students",
            ),
            flex(
                rx.link(
                    "Donate",
                    href=f"{BaseState.host_address}/donate",
                    class_name="text-teal-700 dark:text-zinc-200 cursor-pointer"
                ),
                class_name="flex-row items-center space-x-2 cursor-pointer"
            ),
            class_name="flex-row space-x-8 hidden md:flex ml-8"
        )
    )

def search() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,

        # Shows search if user is logged in
        flex(
            outline_button(
                rx.icon("search", class_name="h-5 w-5"),
                rx.text("Search"),
                disabled=(BaseState.current_location == "/search/hospital"),
                on_click=rx.redirect("/search/hospital"),
                class_name="shadow-lg"
            )
        ),

        # Hides search if user not logged in.
        flex()
    )

def dashboard() -> rx.Component:
    return rx.cond(
        (
            UserState.user_claims_authenticated &
            ~UserState.user_needs_onboarding
        ),

        # Show dashboard if user is logged in.
        flex(
            rx.tooltip(
                outline_button(
                    rx.icon("layout-dashboard", class_name="h-5 w-5"),
                    disabled=(BaseState.current_location == "/dashboard"),
                    on_click=rx.redirect("/dashboard"),
                    class_name="shadow-lg focus:outline-none",
                ),
                content="Dashboard",
                delay_duration=300
            ),
            class_name="hidden md:flex"
        ),
    )

def login_or_account() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,

        # Show account if user is logged in.
        flex(
            rx.tooltip(
                outline_button(
                    rx.icon("circle-user-round", class_name="h-5 w-5"),
                    on_click=rx.redirect("/my-account"),
                    class_name="shadow-lg focus:outline-none"
                ),
                content="My Account",
                delay_duration=300
            ),
            class_name="hidden md:flex"
        ),

        # Show login if user not logged in.
        flex(
            outline_button(
                "Login",
                on_click=rx.redirect("/login"),
                class_name="shadow-lg"
            ),
        )
    )

def mobile_menu() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,

        # Show mobile menu for logged in users.
        rx.cond(
            ~UserState.user_needs_onboarding,

            # Show menu for logged in and onboarded users.
            flex(
                rx.drawer.root(
                    rx.drawer.trigger(
                        outline_button(
                            rx.icon("menu", class_name="h-5 w-5"),
                            class_name="shadow-lg focus:outline-none"
                        )
                    ),
                    rx.drawer.overlay(),
                    rx.drawer.portal(
                        rx.drawer.content(
                            flex(
                                flex(
                                    rx.heading("NurseReports"),
                                    rx.spacer(),
                                    rx.drawer.close(rx.icon("X", cursor="pointer")),
                                    class_name="flex-row justify-center p-8 w-full"
                                ),
                                flex(
                                    link(
                                        "Hospital Search",
                                        href=f"{BaseState.host_address}/search/hospital",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                flex(
                                    link(
                                        "State Summary",
                                        href=f"{BaseState.host_address}/search/state",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                flex(
                                    link(
                                        "Dashboard",
                                        href=f"{BaseState.host_address}/dashboard",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                flex(
                                    link(
                                        "Donate",
                                        href=f"{BaseState.host_address}/donate",
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    class_name="flex p-8 w-full"
                                ),
                                flex(
                                    flex(
                                        link(
                                            "Logout",
                                            class_name="text-zinc-700 cursor-pointer",
                                            on_click=BaseState.event_state_logout
                                        ),
                                        rx.icon("log-out", class_name="h-5 w-5 text-zinc-700"),
                                        class_name="flex-row items-center space-x-4"
                                    ),
                                    class_name="flex-row p-8 w-full"
                                ),
                                class_name="flex-col divide-y divide-zinc-500 w-full"
                            ),
                            class_name="h-full w-full"
                        )
                    ),
                    direction="top",
                ),
                class_name="flex md:hidden cursor-pointer"
            ),

            # Show menu for logged in but not onboarded users.
            flex(
                rx.drawer.root(
                    rx.drawer.trigger(
                        outline_button(
                            rx.icon("menu", class_name="h-5 w-5"),
                            class_name="shadow-lg"
                        )
                    ),
                    rx.drawer.overlay(),
                    rx.drawer.portal(
                        rx.drawer.content(
                            flex(
                                flex(
                                    rx.heading("NurseReports"),
                                    rx.spacer(),
                                    rx.drawer.close(rx.icon("X", cursor="pointer")),
                                    class_name="flex-row justify-center p-8 w-full"
                                ),
                                flex(
                                    flex(
                                        link(
                                            "Logout",
                                            class_name="text-zinc-700 cursor-pointer",
                                            on_click=AuthState.event_state_logout
                                        ),
                                        rx.icon("log-out", class_name="text-zinc-700"),
                                        class_name="space-x-4"
                                    ),
                                    class_name="flex-row p-8 w-full"
                                ),
                                class_name="flex-col divide-y divide-zinc-500"
                            )
                        )
                    ),
                    direction="top"
                ),
                class_name="flex md:hidden cursor-pointer",
            )
        ),

        # Show menu for users not logged in.
        flex(
            rx.drawer.root(
                rx.drawer.trigger(
                    outline_button(
                        rx.icon("menu", class_name="h-5 w-5"),
                        class_name="shadow-lg focus:outline-none"
                    )
                ),
                rx.drawer.overlay(),
                rx.drawer.portal(
                    rx.drawer.content(
                        flex(
                            flex(
                                rx.heading("NurseReports"),
                                rx.spacer(),
                                rx.drawer.close(rx.icon("X", cursor="pointer")),
                                class_name="flex-row justify-center p-8 w-full"
                            ),
                            flex(
                                link(
                                    "Staff",
                                    href=f"{BaseState.host_address}/for-staff",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            flex(
                                link(
                                    "Travelers",
                                    href=f"{BaseState.host_address}/for-travelers",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            flex(
                                link(
                                    "Students",
                                    href=f"{BaseState.host_address}/for-students",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            flex(
                                link(
                                    "Donate",
                                    href=f"{BaseState.host_address}/donate",
                                    class_name="text-zinc-700 cursor-pointer"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            flex(
                                flex(
                                    link(
                                        "Login",
                                        on_click=rx.redirect("/login"),
                                        class_name="text-zinc-700 cursor-pointer"
                                    ),
                                    rx.icon("log-in", class_name="h-5 w-5 text-zinc-700"),
                                    class_name="flex-row items-center space-x-4"
                                ),
                                class_name="flex p-8 w-full"
                            ),
                            class_name="flex-col divide-y divide-zinc-500 w-full"
                        ),
                        class_name="h-full w-full"
                    )
                ),
                direction="top",
            ),
            class_name="flex md:hidden cursor-pointer"
        )
    )