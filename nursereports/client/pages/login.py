from ..components import(
    flex,
    text,
    input,
    link,
    solid_button
)
from ...states import UserState

import reflex as rx


@rx.page(route="/login", title="Nurse Reports")
def login_page() -> rx.Component:
    return flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 dark:from-zinc-800 dark:to-zinc-950 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return flex(
        header(),
        flex(rx.divider(), class_name="pb-3 w-full"),
        create_account(),
        login(),
        class_name="flex-col items-center border dark:border-zinc-700 rounded shadow-lg p-8 space-y-4 w-full max-w-md",
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


def create_account() -> rx.Component:
    return rx.flex(
        text("New to NurseReports.org?"),
        rx.link(
            "Create account here",
            on_click=rx.redirect("/create-account"),
            class_name="text-teal-700 cursor-pointer",
        ),
        class_name="flex-col bg-zinc-100 dark:bg-zinc-800 border border-solid border-zinc-300 dark:border-zinc-700 rounded items-center p-2 w-full",
    )


def login() -> rx.Component:
    return rx.form(
        flex(
            text(
                "Login to your account",
                class_name="text-xl pt-8 font-bold text-zinc-700",
            ),
            flex(
                flex(
                    text("Email", size="2", class_name="pb-1"),
                    input(
                        placeholder="Enter email",
                        name="email",
                        size="3",
                        class_name="w-full",
                        color_scheme="teal"
                    ),
                    class_name="flex-col w-full",
                ),
                flex(
                    text("Password", class_name="text-sm"),
                    input(
                        placeholder="Enter password",
                        name="password",
                        type="password",
                        size="3",
                        class_name="w-full",
                        color_scheme="teal"
                    ),
                    class_name="flex-col space-y-1 w-full",
                ),
                flex(
                    solid_button(
                        "Login",
                        type="submit",
                        size="3",
                        loading=UserState.user_is_loading,
                        class_name="w-full",
                    ),
                    link(
                        "Forgot your password?",
                        on_click=rx.redirect("/login/forgot-password"),
                        class_name="text-sm",
                    ),
                    class_name="flex-col items-center pt-5 space-y-6 w-full",
                ),
                class_name="flex-col items-center space-y-6 w-full",
            ),
            flex(
                rx.divider(),
                text("OR", size="2", padding="6px", white_space="nowrap"),
                rx.divider(),
                class_name="flex-row items-center pt-4 space-x-4 w-full",
            ),
            flex(
                rx.button(
                    rx.image(src="/sso/google_sso.png", class_name="h-16 w-16"),
                    variant="ghost",
                    loading=UserState.user_is_loading,
                    class_name="h-16 w-16 cursor-pointer",
                    on_click=UserState.event_state_login_with_sso("google"),
                ),
                rx.button(
                    rx.image(src="/sso/facebook_sso.png", class_name="h-16 w-16"),
                    variant="ghost",
                    loading=UserState.user_is_loading,
                    class_name="h-16 w-16 cursor-pointer",
                    on_click=UserState.event_state_login_with_sso("facebook"),
                ),
                rx.button(
                    rx.image(src="/sso/linkedin_sso.png", class_name="h-16 w-16"),
                    variant="ghost",
                    loading=UserState.user_is_loading,
                    class_name="h-16 w-16 cursor-pointer",
                    on_click=UserState.event_state_login_with_sso("linkedin_oidc"),
                ),
                class_name="flex-row justify-center pt-3 pb-6 space-x-14 w-full",
            ),
            class_name="flex-col items-center space-y-8 w-full",
        ),
        on_submit=[
            UserState.setvar("user_is_loading", True),
            UserState.event_state_submit_login
        ],
        reset_on_submit=False,
    )
