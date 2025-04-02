from .tailwind import flex, text, link, outline_button

from ...states import AuthState, BaseState, UserState, NavbarState

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
                dashboard(),
                login_or_account(),
                mobile_menu(),
                class_name="flex-row space-x-2",
            ),
            class_name="flex-row items-center justify-between p-3 w-full max-w-screen-xl",
        ),
        class_name="flex-col border border-zinc-100 dark:border-zinc-900 border-b-zinc-200 dark:border-b-zinc-700 bg-zinc-100/50 backdrop-blur-lg dark:bg-zinc-700/50 items-center justify-center sticky top-0 z-10 h-16 w-full",
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
    return rx.flex(
        rx.flex(
            rx.image(
                src="/vector/square-activity.svg", class_name="h-9 md:h-7 w-9 md:w-7"
            ),
            rx.flex(
                rx.text(
                    "Nurse",
                    on_click=rx.cond(
                        AuthState.user_is_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/"),
                    ),
                    class_name="hidden md:flex text-2xl font-bold text-teal-700 dark:text-zinc-200 cursor-pointer",
                ),
                rx.text(
                    "N",
                    on_click=rx.cond(
                        AuthState.user_is_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/"),
                    ),
                    class_name="flex md:hidden text-3xl font-bold text-teal-700 dark:text-zinc-200 cursor-pointer",
                ),
                rx.text(
                    "Reports",
                    on_click=rx.cond(
                        AuthState.user_is_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/"),
                    ),
                    class_name="hidden md:flex text-2xl font-bold text-zinc-700m dark:text-zinc-200 cursor-pointer",
                ),
                rx.text(
                    "R",
                    on_click=rx.cond(
                        AuthState.user_is_authenticated,
                        rx.redirect("/dashboard"),
                        rx.redirect("/"),
                    ),
                    class_name="flex md:hidden text-3xl font-bold text-zinc-700 dark:text-zinc-200 cursor-pointer",
                ),
            ),
            class_name="flex-row items-center",
        ),
        class_name="flex-row items-center space-x-8 justify-center",
    )


def links() -> rx.Component:
    return rx.cond(
        AuthState.user_is_authenticated,
        # Nothing displayed if user is authenticated.
        rx.flex(),
        # Links displayed if user not authenticated.
        rx.flex(
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
            rx.flex(
                rx.link(
                    "Donate",
                    href=f"{BaseState.host_address}/donate",
                    class_name="text-teal-700 dark:text-zinc-200 cursor-pointer",
                ),
                class_name="flex-row items-center space-x-2 cursor-pointer",
            ),
            class_name="flex-row space-x-8 hidden md:flex ml-8",
        ),
    )


def search() -> rx.Component:
    return rx.cond(
        AuthState.user_is_authenticated,
        # Shows search if user is logged in
        flex(
            outline_button(
                rx.icon("search", class_name="h-5 w-5"),
                rx.text("Search"),
                disabled=(BaseState.current_location == "/search/hospital"),
                on_click=rx.redirect("/search/hospital"),
                class_name="shadow-lg",
            )
        ),
        # Hides search if user not logged in.
        flex(),
    )


def dashboard() -> rx.Component:
    return rx.cond(
        (AuthState.user_is_authenticated & ~UserState.user_needs_onboarding),
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
                delay_duration=300,
            ),
            class_name="hidden md:flex",
        ),
    )


def login_or_account() -> rx.Component:
    return rx.cond(
        AuthState.user_is_authenticated,
        # Show account if user is logged in.
        flex(
            rx.tooltip(
                outline_button(
                    rx.icon("circle-user-round", class_name="h-5 w-5"),
                    on_click=rx.redirect("/my-account"),
                    class_name="shadow-lg focus:outline-none",
                ),
                content="My Account",
                delay_duration=300,
            ),
            class_name="hidden md:flex",
        ),
        # Show login if user not logged in.
        flex(
            outline_button(
                "Login", on_click=rx.redirect("/login"), class_name="shadow-lg"
            ),
        ),
    )


def mobile_menu() -> rx.Component:
    return rx.cond(
        AuthState.user_is_authenticated,
        # Show mobile menu for logged in users.
        rx.cond(
            ~UserState.user_needs_onboarding,
            # Show menu for logged in and onboarded users.
            flex(
                rx.drawer.root(
                    rx.drawer.trigger(
                        outline_button(
                            rx.icon("menu", class_name="h-5 w-5"),
                            class_name="shadow-lg focus:outline-none",
                        )
                    ),
                    rx.drawer.overlay(),
                    rx.drawer.portal(
                        rx.drawer.content(
                            flex(
                                rx.flex(
                                    rx.heading("NurseReports"),
                                    rx.spacer(),
                                    rx.drawer.close(rx.icon("X", cursor="pointer")),
                                    class_name="flex-row justify-center p-8 w-full",
                                ),
                                rx.flex(
                                    text("Hospital Search",),
                                    on_click=rx.redirect("/search/hospital"),
                                    class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                                ),
                                rx.flex(
                                    text("Dashboard",),
                                    on_click=rx.redirect("/dashboard"),
                                    class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                                ),
                                rx.flex(
                                    text("Donate",),
                                    on_click=rx.redirect("/donate"),
                                    class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                                ),
                                rx.flex(
                                    rx.flex(
                                        text("Logout"),
                                        rx.icon("log-out", class_name="h-5 w-5 stroke-teal-600 dark:stroke-teal-500"),
                                        class_name="flex-row items-center space-x-4",
                                    ),
                                    on_click=AuthState.logout,
                                    class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                                ),
                                class_name="flex-col divide-y dark:divide-zinc-700 w-full",
                            ),
                            class_name="h-full w-full",
                        )
                    ),
                    direction="top",
                ),
                class_name="flex md:hidden cursor-pointer",
            ),
            # Show menu for logged in but not onboarded users.
            flex(
                rx.drawer.root(
                    rx.drawer.trigger(
                        outline_button(
                            rx.icon("menu", class_name="h-5 w-5"),
                            class_name="shadow-lg",
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
                                    class_name="flex-row justify-center p-8 w-full",
                                ),
                                flex(
                                    flex(
                                        link(
                                            "Logout",
                                            class_name="text-zinc-700 cursor-pointer",
                                            on_click=AuthState.logout,
                                        ),
                                        rx.icon("log-out", class_name="text-zinc-700"),
                                        class_name="space-x-4",
                                    ),
                                    class_name="flex-row p-8 w-full",
                                ),
                                class_name="flex-col divide-y",
                            )
                        )
                    ),
                    direction="top",
                ),
                class_name="flex md:hidden cursor-pointer",
            ),
        ),
        # Show menu for users not logged in.
        flex(
            rx.drawer.root(
                rx.drawer.trigger(
                    outline_button(
                        rx.icon("menu", class_name="h-5 w-5"),
                        class_name="shadow-lg focus:outline-none",
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
                                class_name="flex-row justify-center p-8 w-full",
                            ),
                            rx.flex(
                                text("Staff",),
                                on_click=rx.redirect("/for-staff"),
                                class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                            ),
                            rx.flex(
                                text("Travelers",),
                                on_click=rx.redirect("/for-travelers"),
                                class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                            ),
                            rx.flex(
                                text("Students",),
                                on_click=rx.redirect("/for-students"),
                                class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                            ),
                            rx.flex(
                                text("Donate",),
                                on_click=rx.redirect("/donate"),
                                class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                            ),
                            rx.flex(
                                rx.flex(
                                    text("Login",),
                                    rx.icon(
                                        "log-in",
                                        class_name="h-5 w-5 stroke-teal-600 dark:stroke-teal-500",
                                    ),
                                    class_name="flex-row items-center space-x-4",
                                ),
                                on_click=rx.redirect("/login"),
                                class_name="flex p-8 w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75 cursor-pointer",
                            ),
                            class_name="flex-col divide-y dark:divide-zinc-700 w-full",
                        ),
                        class_name="h-full w-full",
                    )
                ),
                direction="top",
            ),
            class_name="flex md:hidden cursor-pointer",
        ),
    )
