from ...components import (
    solid_button,
    heading,
    text,
    input,
    link,
)
from .navbar import navbar
from ....states import BaseState, UserState

import reflex as rx


@rx.page(
    route="/login",
    title="Nurse Reports",
    on_load=BaseState.event_state_check_expired_login,
)
def login_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        class_name="flex-col items-center bg-white dark:bg-[#0a0a0a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        # Decorative glow orb
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-1/2 "
                "w-[700px] h-[400px] "
                "bg-teal-500/30 dark:bg-teal-600/15 "
                "blur-[140px] rounded-full "
                "pointer-events-none"
            ),
        ),
        # Login card
        rx.flex(
            _logo(),
            _new_account_callout(),
            _login_form(),
            _or_divider(),
            _sso_buttons(),
            class_name=(
                "relative flex-col items-center gap-6 "
                "bg-white dark:bg-[#1a1a1a] "
                "border-0 outline outline-1 outline-neutral-300 dark:outline-neutral-800 "
                "rounded-2xl "
                "p-8 w-full max-w-md z-10"
            ),
        ),
        class_name=(
            "relative flex-col items-center justify-center "
            "flex-1 px-6 py-20 w-full"
        ),
    )


# ---------------------------------------------------------------------------
# Logo
# ---------------------------------------------------------------------------

def _logo() -> rx.Component:
    return rx.flex(
        rx.image(
            src="/vector/square-activity.svg",
            class_name="h-8 w-8 shrink-0",
        ),
        rx.text(
            "Nurse",
            class_name="text-2xl font-semibold text-teal-600 dark:text-teal-500 tracking-tight",
        ),
        rx.text(
            "Reports",
            class_name="text-2xl font-semibold text-neutral-900 dark:text-neutral-100 tracking-tight",
        ),
        on_click=rx.redirect("/"),
        class_name="flex-row items-center gap-2 cursor-pointer mb-2",
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
            on_click=rx.redirect("/create-account"),
            class_name="text-sm font-medium",
        ),
        class_name=(
            "flex-row items-center justify-center gap-2 "
            "bg-teal-500/10 dark:bg-teal-500/[0.07] "
            "border border-neutral-300 dark:border-neutral-800 "
            "rounded-xl px-4 py-3 w-full"
        ),
    )


# ---------------------------------------------------------------------------
# Login form
# ---------------------------------------------------------------------------

def _login_form() -> rx.Component:
    return rx.flex(
        heading(
            "Login to your account",
            class_name="text-xl font-semibold tracking-tight self-start",
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
                            on_click=rx.redirect("/login/forgot-password"),
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
                solid_button(
                    "Login",
                    type="submit",
                    loading=UserState.user_is_loading,
                    class_name="w-full py-3.5 text-base",
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
            class_name="flex-1 h-px bg-neutral-200 dark:bg-neutral-800",
        ),
        text(
            "or continue with",
            class_name="text-xs text-neutral-400 dark:text-neutral-600 px-3 whitespace-nowrap",
        ),
        rx.box(
            class_name="flex-1 h-px bg-neutral-200 dark:bg-neutral-800",
        ),
        class_name="flex-row items-center w-full",
    )


# ---------------------------------------------------------------------------
# SSO buttons
# ---------------------------------------------------------------------------

def _sso_buttons() -> rx.Component:
    return rx.flex(
        _sso_button(
            "/sso/google_sso.png",
            "Google",
            UserState.event_state_login_with_sso("google"),
        ),
        _sso_button(
            "/sso/facebook_sso.png",
            "Facebook",
            UserState.event_state_login_with_sso("facebook"),
        ),
        _sso_button(
            "/sso/linkedin_sso.png",
            "LinkedIn",
            UserState.event_state_login_with_sso("linkedin_oidc"),
        ),
        class_name="flex-row justify-center gap-3 w-full",
    )


def _sso_button(img_src: str, label: str, on_click) -> rx.Component:
    return rx.button(
        rx.flex(
            rx.image(src=img_src, class_name="h-5 w-5 shrink-0"),
            rx.text(label, class_name="text-sm font-medium text-neutral-700 dark:text-neutral-300"),
            class_name="flex-row items-center gap-2",
        ),
        loading=UserState.user_is_loading,
        on_click=[
            UserState.set_user_is_loading(True),
            on_click,
        ],
        class_name=(
            "flex-1 "
            "bg-white dark:bg-[#1a1a1a] "
            "border border-neutral-300 dark:border-neutral-800 "
            "rounded-lg px-4 py-2.5 "
            "hover:bg-neutral-50 dark:hover:bg-neutral-800 "
            "transition-colors duration-150 "
            "cursor-pointer"
        ),
    )
