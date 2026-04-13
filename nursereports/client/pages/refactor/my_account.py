from ...components import (
    button,
    heading,
    text,
    badge,
    icon,
)
from .navbar import navbar
from .footer import footer
from ....states import BaseState, UserState

import reflex as rx

@rx.page(
    route="/my-account",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
    ],
)
def my_account_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        _profile_header(),
        _middle_row(),
        _danger_zone(),
        class_name=(
            "flex-col gap-4 "
            "w-full max-w-screen-lg "
            "mx-auto px-4 md:px-8 py-10"
        ),
    )


# ---------------------------------------------------------------------------
# Section 1 — Profile header
# ---------------------------------------------------------------------------

def _profile_header() -> rx.Component:
    return rx.flex(
        # Wiggle texture overlay
        rx.box(
            class_name=(
                "wiggle-card absolute inset-0 "
                "pointer-events-none"
            ),
        ),
        # Left: avatar + email
        rx.flex(
            rx.avatar(fallback="RN", size="5", color_scheme="green"),
            text(UserState.user_claims_email, weight="semibold", class_name="relative"),
            class_name="flex-row items-center gap-4 relative",
        ),
        # Right: account ID (hidden on mobile)
        rx.flex(
            rx.text(
                "Account ID",
                class_name="text-xs text-neutral-400 dark:text-neutral-600 uppercase tracking-widest mb-1",
            ),
            rx.text(
                UserState.user_claims_id,
                class_name="text-xs font-mono text-neutral-500 dark:text-neutral-400 break-all",
            ),
            class_name="hidden md:flex flex-col items-end max-w-xs relative",
        ),
        class_name=(
            "relative flex-row items-center justify-between "
            "bg-emerald-500/40 dark:bg-white/[0.06] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl p-6 w-full overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Section 2 — Middle row (Professional + Notifications)
# ---------------------------------------------------------------------------

def _middle_row() -> rx.Component:
    return rx.flex(
        _professional_card(),
        _notifications_card(),
        class_name="flex-col md:flex-row gap-4 w-full",
    )


def _professional_card() -> rx.Component:
    return rx.flex(
        _card_header("stethoscope", "Professional Info"),
        _info_row("License Type", UserState.user_info_license_type),
        _info_row("License State", UserState.user_info_license_state),
        _info_row("Experience", UserState.user_info_experience),
        # Specialties row
        rx.flex(
            text(
                "Specialties",
                class_name="text-sm text-neutral-500 dark:text-neutral-400 w-36 shrink-0",
            ),
            rx.flex(
                rx.foreach(
                    UserState.user_info_specialties,
                    lambda x: badge(x, variant="neutral"),
                ),
                class_name="flex-row flex-wrap gap-1.5",
            ),
            class_name="flex-row items-start gap-4 px-5 py-3",
        ),
        class_name=(
            "flex-col flex-1 "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _info_row(label: str, value) -> rx.Component:
    return rx.flex(
        text(
            label,
            class_name="text-sm text-neutral-500 dark:text-neutral-400 w-36 shrink-0",
        ),
        text(value, weight="medium", class_name="text-sm"),
        icon(
            "pencil",
            class_name="h-4 w-4 ml-auto text-neutral-400 dark:text-neutral-500 cursor-pointer hover:text-neutral-600 dark:hover:text-neutral-300 transition-colors",
        ),
        class_name=(
            "flex-row items-center gap-4 "
            "px-5 py-3 "
            "border-b border-neutral-200 dark:border-neutral-800/50"
        ),
    )


def _notifications_card() -> rx.Component:
    return rx.flex(
        _card_header("bell", "Notifications"),
        _notification_row(
            "Status updates",
            "Reports you've submitted and hospital changes",
            UserState.user_info_status_opt_in,
            UserState.event_state_toggle_status_opt_in.throttle(500),
        ),
        _notification_row(
            "Platform updates",
            "New features, improvements, and announcements",
            UserState.user_info_update_opt_in,
            UserState.event_state_toggle_update_opt_in.throttle(500),
        ),
        _notification_row(
            "Community & social",
            "Replies, mentions, and community activity",
            UserState.user_info_social_opt_in,
            UserState.event_state_toggle_social_opt_in.throttle(500),
        ),
        class_name=(
            "flex-col flex-1 "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _notification_row(title: str, description: str, checked, on_change) -> rx.Component:
    return rx.flex(
        rx.flex(
            text(title, weight="medium", class_name="text-sm"),
            rx.text(
                description,
                class_name="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5",
            ),
            class_name="flex-col",
        ),
        rx.switch(
            checked=checked,
            color_scheme="green",
            on_change=on_change
        ),
        class_name=(
            "flex-row items-center justify-between "
            "px-5 py-4 "
            "border-b border-neutral-200 dark:border-neutral-800/50"
        ),
    )


# ---------------------------------------------------------------------------
# Section 3 — Danger zone
# ---------------------------------------------------------------------------

def _danger_zone() -> rx.Component:
    return rx.flex(
        _action_row(
            icon_tag="log-out",
            label="Sign out",
            sublabel="Sign out of your account on this device",
            on_click=BaseState.event_state_logout,
        ),
        class_name=(
            "flex-col w-full "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _action_row(icon_tag: str, label: str, sublabel: str, on_click) -> rx.Component:
    return rx.flex(
        rx.flex(
            icon(icon_tag, class_name="h-5 w-5 shrink-0"),
            rx.flex(
                text(label, weight="medium", class_name="text-sm"),
                rx.text(
                    sublabel,
                    class_name="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5",
                ),
                class_name="flex-col",
            ),
            class_name="flex-row items-center gap-4",
        ),
        icon("chevron-right", muted=True, class_name="h-4 w-4"),
        on_click=on_click,
        class_name=(
            "flex-row items-center justify-between "
            "px-5 py-4 cursor-pointer "
            "hover:bg-neutral-100 dark:hover:bg-white/[0.03] "
            "transition-colors duration-150"
        ),
    )


# ---------------------------------------------------------------------------
# Shared card header helper (matches dashboard pattern)
# ---------------------------------------------------------------------------

def _card_header(icon_tag: str, title: str, action=None) -> rx.Component:
    return rx.flex(
        rx.box(
            class_name="absolute inset-0 pointer-events-none",
        ),
        rx.flex(
            icon(icon_tag, accent=True, class_name="h-5 w-5 relative"),
            heading(title, size="sm", class_name="relative"),
            class_name="flex-row items-center gap-2",
        ),
        action or rx.fragment(),
        class_name=(
            "relative flex-row items-center justify-between "
            "px-5 py-4 overflow-hidden bg-emerald-500/10 dark:bg-white/[0.03] "
            "border-b border-neutral-300 dark:border-neutral-800/50"
        ),
    )
