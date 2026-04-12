from ..components import (
    button,
    heading,
    text,
    input,
    link,
)
from .refactor.navbar import navbar
from ...states import BaseState, UserState

import reflex as rx

_WIGGLE_STYLE = rx.html("""
<style>
  .wiggle-texture {
    background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='9' height='22'><path d='M4.5 0 Q7.5 5.5 4.5 11 Q1.5 16.5 4.5 22' stroke='%2386a88e' stroke-width='0.75' fill='none'/></svg>");
    background-repeat: repeat;
    background-size: 9px 22px;
  }
</style>
""")


@rx.page(
    route="/login/forgot-password",
    title="Nurse Reports"
)
def forgot_password_page() -> rx.Component:
    return rx.flex(
        _WIGGLE_STYLE,
        navbar(),
        _content(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        # Wiggle texture layer
        rx.box(
            class_name=(
                "wiggle-texture "
                "absolute inset-0 "
                "opacity-60 dark:opacity-10 "
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
            _recovery_form(),
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


def _recovery_form() -> rx.Component:
    return rx.flex(
        heading("Password Recovery", size="sm", class_name="self-start"),
        rx.form(
            rx.flex(
                rx.flex(
                    text("Email", class_name="text-sm font-medium mb-1.5"),
                    input(
                        placeholder="Enter your email",
                        name="email",
                        type="email",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                button(
                    "Recover Password",
                    type="submit",
                    color="emerald",
                    size="md",
                    width="full",
                    loading=UserState.user_is_loading,
                ),
                class_name="flex-col gap-4 w-full",
            ),
            on_submit=BaseState.event_state_recover_password,
            reset_on_submit=True,
            class_name="w-full",
        ),
        class_name="flex-col items-center gap-4 w-full",
    )


def _back_to_login() -> rx.Component:
    return rx.flex(
        text("Remember your password?", class_name="text-sm"),
        link(
            "Sign in",
            accent=True,
            href="/login",
            class_name="text-sm font-medium",
        ),
        class_name="flex-row items-center justify-center gap-2",
    )
