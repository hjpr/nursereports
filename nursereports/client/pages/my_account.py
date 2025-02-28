from ..components import (
    flex,
    footer,
    navbar,
    text,
)
from ...states import BaseState, UserState

import reflex as rx


@rx.page(
    route="/my-account",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login
    ]
)
def my_account_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col dark:bg-zinc-900 items-center w-full min-h-screen",
    )


def content() -> rx.Component:
    return rx.flex(
        heading(),
        account(),
        class_name="flex-col grow items-center space-y-4 md:space-y-12 px-4 py-4 md:py-20 w-full md:max-w-screen-md",
    )

def heading() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("circle-user-round", class_name="h-6 w-6 stroke-teal-800"),
            text("My Account", class_name="text-2xl font-bold"),
            class_name="bg-transparent flex-row items-center space-x-2",
        ),
        class_name="flex-col items-center border rounded shadow-lg dark:border-zinc-700 bg-zinc-100 dark:bg-zinc-800 p-4 w-full",
    )

def account() -> rx.Component:
    return flex(
        rx.flex(

            # Avatar panel.
            rx.flex(
                rx.avatar(size="7", fallback="RN", color_scheme="teal", class_name="mb-4"),
                rx.flex(
                    rx.icon("mail", class_name="h-4 w-4 stroke-zinc-700"),
                    rx.text(UserState.user_claims_email, class_name="text-sm"),
                    class_name="flex-row items-center space-x-4 w-full"
                ),
                rx.flex(
                    rx.icon("square-user-round", class_name="h-4 w-4 stroke-zinc-700"),
                    rx.text(UserState.user_claims_id, class_name="text-sm"),
                    class_name="space-x-4 w-full"
                ),
                class_name="flex-col p-8 space-y-2 w-full"
            ),

            # User info panel.
            rx.flex(
                rx.flex(
                    rx.text("User Info", class_name="font-bold"),
                    class_name="justify-center bg-zinc-100 dark:bg-zinc-800 p-2"
                ),
                rx.flex(
                    rx.text(f"License Type: {UserState.user_info_license_type}", class_name="text-sm"),
                    rx.text(f"License State: {UserState.user_info_license_state}", class_name="text-sm"),
                    rx.text(f"Experience: {UserState.user_info_experience}", class_name="text-sm"),
                    class_name="flex-col space-y-2 p-4 w-full"
                ),
                rx.flex(
                    rx.text("Specialties", class_name="font-bold"),
                    class_name="justify-center bg-zinc-100 dark:bg-zinc-800 p-2"
                ),
                rx.flex(
                    rx.foreach(
                        UserState.user_info_specialties,
                        lambda x: rx.badge(x, color_scheme="teal", class_name="mr-2")
                    ),
                    class_name="flex-row inline space-y-2 p-4 w-full"
                ),
                class_name="flex-col divide-y w-full"
            ),

            class_name="flex-col md:flex-row divide-y md:divide-y-0 md:divide-x w-full"
        ),
        logout(),
        class_name="flex-col border rounded shadow-lg dark:border-zinc-500 bg-zinc-100 dark:bg-zinc-800 divide-y w-full",
    )

def logout() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("Log out", class_name="font-bold select-none"),
            on_click=rx.redirect("/logout/user"),
            class_name="flex-row items-center justify-center space-x-2 p-4 cursor-pointer"
        ),
        class_name="flex-col w-full active:bg-zinc-200 dark:active:bg-zinc-700 transition-colors duration-75"
    )