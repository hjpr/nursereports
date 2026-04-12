from ..components import (
    button,
    heading,
    text,
)
from .refactor.navbar import navbar

import reflex as rx

@rx.page(
    route="/login/forgot-password/confirmation",
    title="Nurse Reports",
)
def forgot_password_confirmation_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        # Wiggle texture layer
        rx.box(
            class_name=(
                "wiggle-surface absolute inset-0 "
                "pointer-events-none"
            ),
        ),
        # White blob — light mode only
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-1/2 "
                "w-[680px] h-[480px] "
                "bg-white/80 dark:bg-transparent "
                "blur-[60px] rounded-full "
                "pointer-events-none"
            ),
        ),
        # Emerald glow
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-1/2 "
                "w-[700px] h-[400px] "
                "bg-emerald-400/30 dark:bg-emerald-600/15 "
                "blur-[160px] rounded-full "
                "pointer-events-none"
            ),
        ),
        # Card
        rx.flex(
            _confirmation(),
            _back_to_login(),
            class_name=(
                "relative flex-col items-center gap-5 "
                "bg-emerald-100 dark:bg-[#0f1f13] "
                "border border-neutral-300 dark:border-neutral-800 "
                "rounded-2xl "
                "p-7 w-full max-w-md z-10"
            ),
        ),
        class_name=(
            "relative flex-col items-center justify-center "
            "flex-1 px-6 py-20 w-full overflow-hidden"
        ),
    )


def _confirmation() -> rx.Component:
    return rx.flex(
        heading("Check your email", size="sm", class_name="self-start"),
        text("We just sent you an email link for a one-time login."),
        text(
            "You can access your account options to change your password after login."
        ),
        class_name="flex-col gap-3 w-full",
    )


def _back_to_login() -> rx.Component:
    return button(
        rx.icon("arrow-left", class_name="h-4 w-4"),
        "Go to Login",
        variant="outline",
        size="md",
        width="full",
        on_click=rx.redirect("/login", replace=True),
    )
