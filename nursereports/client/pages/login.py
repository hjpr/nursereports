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
        rx.flex(
            rx.divider(),
            class_name="pb-3 w-full"
        ),
        create_account(),
        login(),
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

def create_account() -> rx.Component:
    return rx.flex(
        rx.text("New to NurseReports.org?"),
        rx.link(
            "Create account here",
            on_click=rx.redirect("/create-account"),
            class_name="cursor-pointer"
            ),
        class_name="flex-col border rounded bg-teal-100 items-center p-2 w-full"
    )


def login() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("Login to your account", class_name="text-xl pt-8 font-bold"),
            rx.flex(
                rx.flex(
                    rx.text("Email", size="2", class_name="pb-1"),
                    rx.input(
                        placeholder="Enter email",
                        name="email",
                        size="3",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                rx.flex(
                    rx.text("Password", class_name="text-sm"),
                    rx.input(
                        placeholder="Enter password",
                        name="password",
                        type="password",
                        size="3",
                        class_name="w-full",
                    ),
                    class_name="flex-col space-y-1 w-full",
                ),
                rx.flex(
                    rx.button(
                        "Login",
                        type="submit",
                        size="3",
                        loading=BaseState.is_loading,
                        class_name="w-full",
                    ),
                    rx.link(
                        "Forgot your password?",
                        on_click=rx.redirect("/login/forgot-password"),
                        class_name="text-sm cursor-pointer"
                    ),
                    class_name="flex-col items-center pt-5 space-y-6 w-full",
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
                    loading=BaseState.is_loading,
                    class_name="h-16 w-16 cursor-pointer",
                    on_click=LoginState.event_state_login_with_sso("google"),
                ),
                rx.button(
                    rx.image(src="/sso/facebook_sso.png", class_name="h-16 w-16"),
                    variant="ghost",
                    loading=BaseState.is_loading,
                    class_name="h-16 w-16 cursor-pointer",
                    on_click=LoginState.event_state_login_with_sso("facebook"),
                ),
                rx.button(
                    rx.image(src="/sso/linkedin_sso.png", class_name="h-16 w-16"),
                    variant="ghost",
                    loading=BaseState.is_loading,
                    class_name="h-16 w-16 cursor-pointer",
                    on_click=LoginState.event_state_login_with_sso("linkedin_oidc"),
                ),
                class_name="flex-row justify-center pt-3 pb-6 space-x-14 w-full",
            ),
            class_name="flex-col items-center space-y-8 w-full",
        ),
        on_submit=LoginState.event_state_submit_login,
        reset_on_submit=True
    )