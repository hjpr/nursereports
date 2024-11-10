from ...states import BaseState, LoginState

import reflex as rx


@rx.page(route="/login", title="Nurse Reports", on_load=BaseState.event_state_auth_flow)
def login_page() -> rx.Component:
    return rx.flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-200 to-blue-100 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        rx.divider(),
        login(),
        class_name="flex-col items-center rounded shadow-lg bg-white p-8 space-y-6 w-full max-w-md",
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
    return rx.form(
        rx.flex(
            rx.tabs.root(
                rx.center(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            "Login",
                            value="login",
                            on_click=LoginState.set_current_tab("login"),
                        ),
                        rx.tabs.trigger(
                            "Create Account",
                            value="create_account",
                            on_click=LoginState.set_current_tab("create_account"),
                        ),
                        size="2",
                    ),
                    class_name="w-full",
                ),
                rx.tabs.content(login_tab(), value="login"),
                rx.tabs.content(create_account_tab(), value="create_account"),
                value=LoginState.current_tab,
                class_name="w-full",
            ),
            class_name="w-full md:max-w-640",
        ),
        on_submit=LoginState.event_state_submit_login,
    )


def login_tab() -> rx.Component:
    return rx.flex(
        rx.text("Login to your account", class_name="text-xl pt-8 font-bold"),
        rx.flex(
            rx.flex(
                rx.text("Email", size="2", padding="0 0 0 12px"),
                rx.input(
                    placeholder="Enter email",
                    name="login_email",
                    size="3",
                    required=True,
                    class_name="w-full",
                ),
                class_name="flex-col w-full",
            ),
            rx.flex(
                rx.text("Password", size="2", padding="0 0 0 12px"),
                rx.input(
                    placeholder="Enter password",
                    name="login_password",
                    type="password",
                    size="3",
                    required=True,
                    class_name="w-full",
                ),
                class_name="flex-col w-full",
            ),
            error_login(),
            rx.flex(
                rx.button(
                    "Login",
                    type="submit",
                    size="3",
                    loading=~rx.State.is_hydrated,
                    class_name="w-full",
                    on_click=rx.State.set_is_hydrated(False),
                ),
                class_name="flex-col pt-5 w-full",
            ),
            class_name="flex-col items-center space-y-6 w-full",
        ),
        rx.flex(
            rx.divider(),
            rx.text("OR", size="2", padding="6px", white_space="nowrap"),
            rx.divider(),
            class_name="flex-row items-center pt-4 space-x-4 w-full",
        ),
        rx.flex(
            rx.button(
                rx.image(src="/sso/google_sso.png", class_name="h-16 w-16"),
                variant="ghost",
                loading=~rx.State.is_hydrated,
                class_name="h-16 w-16 cursor-pointer",
                on_click=[
                    rx.State.set_is_hydrated(False),
                    LoginState.event_state_login_with_sso("google"),
                ],
            ),
            rx.button(
                rx.image(src="/sso/facebook_sso.png", class_name="h-16 w-16"),
                variant="ghost",
                loading=~rx.State.is_hydrated,
                class_name="h-16 w-16 cursor-pointer",
                on_click=[
                    rx.State.set_is_hydrated(False),
                    LoginState.event_state_login_with_sso("facebook"),
                ],
            ),
            rx.button(
                rx.image(src="/sso/linkedin_sso.png", class_name="h-16 w-16"),
                variant="ghost",
                loading=~rx.State.is_hydrated,
                class_name="h-16 w-16 cursor-pointer",
                on_click=[
                    rx.State.set_is_hydrated(False),
                    LoginState.event_state_login_with_sso("linkedin_oidc"),
                ],
            ),
            class_name="flex-row justify-center pt-3 pb-6 space-x-14 w-full",
        ),
        class_name="flex-col items-center space-y-8 w-full",
    )


def error_login() -> rx.Component:
    return rx.cond(
        LoginState.error_message_login,
        rx.callout(
            LoginState.error_message_login,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            margin="20px 0 0 0",
        ),
    )


def create_account_tab() -> rx.Component:
    return rx.flex(
        rx.text("Create new account", class_name="text-xl pt-8 font-bold"),
        rx.flex(
            rx.flex(
                rx.text("Email", size="2", padding="0 0 0 12px"),
                rx.input(
                    placeholder="Enter email",
                    name="create_account_email",
                    size="3",
                    required=True,
                    class_name="w-full",
                ),
                class_name="flex-col w-full",
            ),
            rx.flex(
                rx.flex(
                    rx.text("Password", size="2", padding="0 0 0 12px"),
                    rx.input(
                        placeholder="Enter password",
                        name="create_account_password",
                        type="password",
                        size="3",
                        required=True,
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                rx.flex(
                    rx.text("Confirm password", size="2", padding="0 0 0 12px"),
                    rx.input(
                        placeholder="Re-enter password",
                        name="create_account_password_confirm",
                        type="password",
                        size="3",
                        required=True,
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                class_name="flex-col space-y-6 w-full",
            ),
            error_create_account(),
            rx.flex(
                rx.button(
                    "Create account", type="submit", size="3", class_name="w-full"
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
    )


def error_create_account() -> rx.Component:
    return rx.cond(
        LoginState.error_message_create_account,
        rx.callout(
            LoginState.error_message_create_account,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            margin="20px 0 0 0",
        ),
    )
