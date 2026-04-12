from ...components import (
    button,
    heading,
    text,
    input,
    link,
)
from .navbar import navbar
from ....states import BaseState, UserState

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
    route="/login",
    title="Nurse Reports",
    on_load=BaseState.event_state_check_expired_login,
)
def login_page() -> rx.Component:
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
        # Login card
        rx.flex(
            _sso_buttons(),
            _or_divider(),
            _login_form(),
            _new_account_callout(),
            class_name=(
                "relative flex-col items-center gap-5 "
                "bg-neutral-100/80 dark:bg-neutral-900/80 "
                "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
                "rounded-2xl "
                "p-7 w-full max-w-md z-10"
            ),
        ),
        class_name=(
            "relative flex-col items-center justify-center "
            "flex-1 px-6 py-20 w-full overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# New account callout
# ---------------------------------------------------------------------------

def _new_account_callout() -> rx.Component:
    return rx.flex(
        text(
            "New to NurseReports?",
            class_name="text-sm",
        ),
        link(
            "Create a free account",
            accent=True,
            href="/create-account",
            class_name="text-sm font-medium",
        ),
        class_name="flex-row items-center justify-center gap-2",
    )


# ---------------------------------------------------------------------------
# Login form
# ---------------------------------------------------------------------------

def _login_form() -> rx.Component:
    return rx.flex(
        heading(
            "Sign in with email",
            size="sm",
            class_name="self-start",
        ),
        rx.form(
            rx.flex(
                # Email field
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
                # Password field
                rx.flex(
                    rx.flex(
                        text("Password", class_name="text-sm font-medium"),
                        link(
                            "Forgot password?",
                            href="/login/forgot-password",
                            class_name="text-xs ml-auto",
                        ),
                        class_name="flex-row items-center w-full mb-1.5",
                    ),
                    input(
                        placeholder="Enter your password",
                        name="password",
                        type="password",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                # Submit
                button(
                    "Login",
                    type="submit",
                    color="emerald",
                    size="md",
                    width="full",
                    loading=UserState.user_is_loading,
                ),
                class_name="flex-col gap-4 w-full",
            ),
            on_submit=[
                UserState.setvar("user_is_loading", True),
                UserState.event_state_submit_login,
            ],
            reset_on_submit=False,
            class_name="w-full",
        ),
        class_name="flex-col items-center gap-4 w-full",
    )


# ---------------------------------------------------------------------------
# OR divider
# ---------------------------------------------------------------------------

def _or_divider() -> rx.Component:
    return rx.flex(
        rx.box(
            class_name="flex-1 h-px bg-neutral-200 dark:bg-neutral-800/50",
        ),
        text(
            "or",
            class_name="text-xs text-neutral-400 dark:text-neutral-600 px-3 whitespace-nowrap",
        ),
        rx.box(
            class_name="flex-1 h-px bg-neutral-200 dark:bg-neutral-800/50",
        ),
        class_name="flex-row items-center w-full",
    )


# ---------------------------------------------------------------------------
# SSO buttons
# ---------------------------------------------------------------------------

def _sso_buttons() -> rx.Component:
    return rx.flex(
        _sso_button("/sso/google_sso.png", UserState.event_state_login_with_sso("google")),
        _sso_button("/sso/facebook_sso.png", UserState.event_state_login_with_sso("facebook")),
        _sso_button("/sso/linkedin_sso.png", UserState.event_state_login_with_sso("linkedin_oidc")),
        class_name="flex-row justify-center gap-6 w-full",
    )


def _sso_button(img_src: str, on_click) -> rx.Component:
    return rx.el.button(
        rx.cond(
            UserState.user_is_loading,
            rx.spinner(size="3"),
            rx.image(src=img_src, class_name="h-12 w-12"),
        ),
        on_click=[
            UserState.set_user_is_loading(True),
            on_click,
        ],
        class_name=(
            "flex items-center justify-center "
            "h-16 w-16 "
            "bg-neutral-100 dark:bg-white/[0.04] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-full "
            "hover:bg-neutral-200 dark:hover:bg-white/[0.07] "
            "transition-colors duration-150 "
            "cursor-pointer"
        ),
    )
