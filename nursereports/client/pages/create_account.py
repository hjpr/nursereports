from ..components import (
    button,
    heading,
    text,
    input,
    link,
)
from .refactor.navbar import navbar
from ...states import UserState, BaseState

import reflex as rx

@rx.page(
    route="/create-account",
    title="Nurse Reports",
)
def create_account_page() -> rx.Component:
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
            _sso_buttons(),
            _or_divider(),
            _create_account_form(),
            _login_callout(),
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


# ---------------------------------------------------------------------------
# OR divider
# ---------------------------------------------------------------------------

def _or_divider() -> rx.Component:
    return rx.flex(
        rx.box(class_name="flex-1 h-px bg-neutral-300 dark:bg-neutral-800"),
        text(
            "or",
            class_name="text-xs text-neutral-400 dark:text-neutral-600 px-3 whitespace-nowrap",
        ),
        rx.box(class_name="flex-1 h-px bg-neutral-300 dark:bg-neutral-800"),
        class_name="flex-row items-center w-full",
    )


# ---------------------------------------------------------------------------
# Create account form
# ---------------------------------------------------------------------------

def _create_account_form() -> rx.Component:
    return rx.flex(
        heading("Create your account", size="sm", class_name="self-start"),
        rx.form(
            rx.flex(
                # Email
                rx.flex(
                    text("Email", class_name="text-sm font-medium mb-1.5"),
                    input(
                        placeholder="Enter your email",
                        name="create_account_email",
                        type="email",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                # Password
                rx.flex(
                    text("Password", class_name="text-sm font-medium mb-1.5"),
                    input(
                        placeholder="Enter your password",
                        name="create_account_password",
                        type="password",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                # Confirm password
                rx.flex(
                    text("Confirm password", class_name="text-sm font-medium mb-1.5"),
                    input(
                        placeholder="Re-enter your password",
                        name="create_account_password_confirm",
                        type="password",
                        class_name="w-full",
                    ),
                    class_name="flex-col w-full",
                ),
                text(
                    "At least 8 characters with letters and numbers.",
                    class_name="text-xs text-neutral-400 dark:text-neutral-600 text-center",
                ),
                button(
                    "Create account",
                    type="submit",
                    color="emerald",
                    size="md",
                    width="full",
                    loading=UserState.user_is_loading,
                ),
                class_name="flex-col gap-4 w-full",
            ),
            on_submit=UserState.event_state_create_account,
            reset_on_submit=False,
            class_name="w-full",
        ),
        class_name="flex-col items-center gap-4 w-full",
    )


# ---------------------------------------------------------------------------
# Login callout
# ---------------------------------------------------------------------------

def _login_callout() -> rx.Component:
    return rx.flex(
        text("Already have an account?", class_name="text-sm"),
        link(
            "Sign in",
            accent=True,
            href="/login",
            class_name="text-sm font-medium",
        ),
        class_name="flex-row items-center justify-center gap-2",
    )
