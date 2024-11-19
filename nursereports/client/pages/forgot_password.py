from ...states import BaseState, UserState

import reflex as rx


@rx.page(
    route="/login/forgot-password",
    title="Nurse Reports",
    on_load=BaseState.event_state_auth_flow,
)
def forgot_password_page() -> rx.Component:
    return rx.flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        header(),
        rx.flex(rx.divider(), class_name="w-full"),
        forgot_password(),
        nav_back(),
        class_name="flex-col items-center rounded shadow-lg bg-white p-8 space-y-4 w-full max-w-md",
    )


def header() -> rx.Component:
    return rx.flex(
        rx.image(src="/vector/square-activity.svg", class_name="h-9 w-9 mb-1"),
        rx.text(
            "Nurse",
            on_click=rx.redirect("/"),
            class_name="text-4xl cursor-pointer text-teal-700 pb-1 font-bold",
        ),
        rx.text(
            "Reports",
            on_click=rx.redirect("/"),
            class_name="text-4xl cursor-pointer text-zinc-700 pb-1 font-bold",
        ),
        class_name="flex-row items-center justify-center w-full",
    )


def forgot_password() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("Password Recovery", class_name="text-xl pt-6 font-bold"),
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
                    rx.button(
                        "Recover Password",
                        type="submit",
                        size="3",
                        loading=UserState.user_is_loading,
                        class_name="w-full",
                    ),
                    class_name="flex-col items-center pt-5 w-full",
                ),
                class_name="flex-col items-center space-y-6 w-full",
            ),
            class_name="flex-col items-center space-y-6 w-full",
        ),
        on_submit=BaseState.event_state_recover_password,
        reset_on_submit=True,
    )


def nav_back() -> rx.Component:
    return rx.flex(
        rx.button(
            rx.icon("arrow-left"),
            "Go to Login",
            size="3",
            loading=UserState.user_is_loading,
            variant="outline",
            on_click=rx.redirect("/login", replace=True),
            class_name="w-full",
        ),
        class_name="w-full",
    )
