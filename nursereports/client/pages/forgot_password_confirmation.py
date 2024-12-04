from ..components import (
    flex,
    text,
    solid_button
)
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/login/forgot-password/confirmation",
    title="Nurse Reports",
    on_load=BaseState.event_state_auth_flow,
)
def forgot_password_confirmation_page() -> rx.Component:
    return flex(
        content(),
        class_name="flex-col bg-gradient-to-b from-teal-100 to-cyan-100 dark:from-zinc-800 dark:to-zinc-950 items-center justify-center p-4 min-h-screen w-full",
    )


def content() -> rx.Component:
    return flex(
        header(),
        flex(rx.divider(), class_name="pb-3 w-full"),
        confirmation(),
        flex(
            solid_button(
                rx.icon("arrow-left"),
                "Go to Login",
                size="3",
                on_click=rx.redirect("/login", replace=True),
                class_name="w-full",
            ),
            class_name="pt-4 pb-2 w-full",
        ),
        class_name="flex-col items-center rounded shadow-lg bg-white p-8 space-y-4 w-full max-w-md",
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


def confirmation() -> rx.Component:
    return flex(
        text("We just sent you an email link for a one-time login."),
        text(
            "You can access your account options to change your password after login."
        ),
        class_name="flex-col space-y-4 w-full",
    )
