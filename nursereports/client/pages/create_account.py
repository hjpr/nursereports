from ...states import BaseState, LoginState

import reflex as rx


@rx.page(route="/create-account", title="Nurse Reports", on_load=BaseState.event_state_auth_flow)
def create_account_page() -> rx.Component:
    return rx.flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-200 to-blue-100 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        rx.flex(
            rx.divider(),
            class_name="pb-3 w-full"
        ),
        login(),
        create_account(),
        class_name="flex-col items-center rounded shadow-lg bg-white p-8 space-y-4 w-full max-w-md",
    )


def header() -> rx.Component:
    return rx.flex(
        rx.image(src="/vector/square-activity.svg", class_name="h-9 w-9 mb-0.5 mr-2"),
        rx.text(
            "Nurse Reports", 
            on_click=rx.redirect("/"),
            class_name="text-4xl cursor-pointer text-teal-700 pb-1 font-bold"
        ),
        class_name="flex-row items-center justify-center w-full",
    )

def login() -> rx.Component:
    return rx.flex(
        rx.text("Already have an account?"),
        rx.link(
            "Go to login",
            on_click=rx.redirect("/login"),
            class_name="cursor-pointer"
            ),
        class_name="flex-col border rounded bg-teal-100 items-center p-2 w-full"
    )


def create_account() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("Create new account", class_name="text-xl pt-8 font-bold"),
            rx.flex(
                rx.flex(
                    rx.text("Email", size="2", class_name="pb-1"),
                    rx.input(
                        placeholder="Enter email",
                        name="create_account_email",
                        size="3",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                rx.flex(
                    rx.flex(
                        rx.text("Password", size="2", class_name="pb-1"),
                        rx.input(
                            placeholder="Enter password",
                            name="create_account_password",
                            type="password",
                            size="3",
                            class_name="w-full",
                        ),
                        class_name="flex-col w-full",
                    ),
                    rx.flex(
                        rx.text("Confirm password", size="2", class_name="pb-1"),
                        rx.input(
                            placeholder="Re-enter password",
                            name="create_account_password_confirm",
                            type="password",
                            size="3",
                            class_name="w-full",
                        ),
                        class_name="flex-col w-full",
                    ),
                    rx.flex(
                        rx.text(
                            "Passwords should be at least 8 characters long and contain numbers + letters",
                            class_name="text-sm text-center"
                        ),
                        class_name="w-full"
                    ),
                    class_name="flex-col space-y-6 w-full",
                ),
                rx.flex(
                    rx.button(
                        "Create account",
                        type="submit",
                        size="3",
                        class_name="w-full",
                        loading=BaseState.is_loading
                    ),
                    class_name="flex-col pt-5 pb-6 w-full",
                ),
                class_name="flex-col items-center space-y-6 w-full",
            ),
            rx.divider(),
            rx.center(
                rx.flex(
                    rx.link(
                        "Privacy Policy",
                        size="2",
                        on_click=rx.redirect("/policy/privacy"),
                        class_name="cursor-pointer"
                    ),
                    rx.divider(orientation="vertical"),
                    rx.link(
                        "AI Policy",
                        size="2",
                        on_click=rx.redirect("/policy/ai"),
                        class_name="cursor-pointer"
                    ),
                    class_name="flex-row items-center justify-center p-2 mb-1 space-x-8 w-full"
                )
            ),
            class_name="flex-col items-center space-y-8 w-full",
        ),
        on_submit=LoginState.event_state_create_account,
        reset_on_submit=True
    )