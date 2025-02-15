from ..components import(
    flex,
    text,
    input,
    link,
    solid_button
)
from ...states import UserState

import reflex as rx


@rx.page(
    route="/create-account",
    title="Nurse Reports",
)
def create_account_page() -> rx.Component:
    return flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 dark:from-zinc-800 dark:to-zinc-950 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return flex(
        header(),
        flex(rx.divider(), class_name="pb-3 w-full"),
        login(),
        create_account(),
        class_name="flex-col items-center border rounded shadow-lg p-8 space-y-4 w-full max-w-md",
    )


def header() -> rx.Component:
    return flex(
        rx.image(src="/vector/square-activity.svg", class_name="h-9 w-9 mb-1"),
        rx.text(
            "Nurse",
            on_click=rx.redirect("/"),
            class_name="text-4xl cursor-pointer text-teal-700 dark:text-zinc-200 pb-1 font-bold",
        ),
        rx.text(
            "Reports",
            on_click=rx.redirect("/"),
            class_name="text-4xl cursor-pointer text-zinc-700 dark:text-zinc-200 pb-1 font-bold",
        ),
        class_name="flex-row items-center justify-center w-full",
    )


def login() -> rx.Component:
    return rx.flex(
        text("Already have an account?"),
        rx.link(
            "Go to login", on_click=rx.redirect("/login"), class_name="text-teal-700 cursor-pointer"
        ),
        class_name="flex-col bg-zinc-100 dark:bg-zinc-800 border border-solid border-zinc-300 dark:border-zinc-700 rounded items-center p-2 w-full",
    )


def create_account() -> rx.Component:
    return rx.form(
        flex(
            text(
                "Create new account", class_name="text-xl pt-8 font-bold text-zinc-700"
            ),
            flex(
                flex(
                    text("Email", size="2", class_name="pb-1"),
                    input(
                        placeholder="Enter email",
                        name="create_account_email",
                        size="3",
                        class_name="w-full",
                        color_scheme="teal"
                    ),
                    class_name="flex-col w-full",
                ),
                flex(
                    flex(
                        text("Password", size="2", class_name="pb-1"),
                        input(
                            placeholder="Enter password",
                            name="create_account_password",
                            type="password",
                            size="3",
                            class_name="w-full",
                            color_scheme="teal"
                        ),
                        class_name="flex-col w-full",
                    ),
                    flex(
                        text("Confirm password", size="2", class_name="pb-1"),
                        input(
                            placeholder="Re-enter password",
                            name="create_account_password_confirm",
                            type="password",
                            size="3",
                            class_name="w-full",
                            color_scheme="teal"
                        ),
                        class_name="flex-col w-full",
                    ),
                    flex(
                        text(
                            "Passwords should be at least 8 characters long and contain numbers + letters",
                            class_name="text-sm text-center",
                        ),
                        class_name="w-full",
                    ),
                    class_name="flex-col space-y-6 w-full",
                ),
                flex(
                    solid_button(
                        "Create account",
                        type="submit",
                        size="3",
                        class_name="w-full",
                        loading=UserState.user_is_loading,
                    ),
                    class_name="flex-col pt-5 pb-6 w-full",
                ),
                class_name="flex-col items-center space-y-6 w-full",
            ),
            rx.divider(),
            rx.center(
                flex(
                    link(
                        "Privacy Policy",
                        size="2",
                        on_click=rx.redirect("/policy/privacy"),
                        class_name="cursor-pointer",
                    ),
                    rx.divider(orientation="vertical"),
                    link(
                        "AI Policy",
                        size="2",
                        on_click=rx.redirect("/policy/ai"),
                        class_name="cursor-pointer",
                    ),
                    class_name="flex-row items-center justify-center p-2 mb-1 space-x-8 w-full",
                )
            ),
            class_name="flex-col items-center space-y-8 w-full",
        ),
        on_submit=UserState.event_state_create_account,
    )
