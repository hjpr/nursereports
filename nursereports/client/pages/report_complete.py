from ..components import (
    button,
    confetti,
    heading,
    icon,
    login_protected,
    text,
)
from .navbar import navbar
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/report/[report_mode]/complete",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
    ],
)
@login_protected
def complete_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        _fireworks(),
        class_name=(
            "flex-col items-center "
            "bg-neutral-50 dark:bg-[#07100a] "
            "min-h-screen w-full"
        ),
    )


def _content() -> rx.Component:
    return rx.flex(
        _hero(),
        _share_card(),
        _dashboard_card(),
        class_name=(
            "flex-col gap-4 "
            "w-full max-w-screen-sm "
            "mx-auto px-4 pt-4 md:pt-10 pb-10"
        ),
    )


def _hero() -> rx.Component:
    return rx.flex(
        rx.box(class_name="absolute inset-0 pointer-events-none"),
        rx.flex(
            icon("party-popper", accent=True, class_name="h-8 w-8 relative"),
            heading(
                "Report submitted!",
                size="xl",
                class_name="relative",
            ),
            text(
                "Every report adds to transparency and accountability across the US. "
                "Don't forget to share this site with your friends and colleagues.",
                size="sm",
                class_name="text-neutral-600 dark:text-neutral-400 relative",
            ),
            class_name="flex-col gap-2 relative",
        ),
        class_name=(
            "relative flex-col gap-4 px-5 py-6 overflow-hidden "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl"
        ),
    )


def _share_card() -> rx.Component:
    _divider = "border-b border-neutral-300 dark:border-neutral-800/50"

    def _share_row(icon_tag: str, label: str, url: str) -> rx.Component:
        return rx.flex(
            icon(icon_tag, class_name="h-5 w-5 shrink-0"),
            text(label, size="sm", weight="medium"),
            rx.spacer(),
            icon("arrow-right", muted=True, class_name="h-4 w-4 shrink-0"),
            on_click=rx.redirect(url),
            class_name=(
                f"flex-row items-center gap-3 px-5 py-4 cursor-pointer {_divider} "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800/40 "
                "transition-colors duration-150"
            ),
        )

    return rx.flex(
        # Card header
        rx.flex(
            rx.box(class_name="absolute inset-0 pointer-events-none"),
            rx.flex(
                icon("share-2", accent=True, class_name="h-5 w-5 relative"),
                heading("Share to...", size="sm", class_name="relative"),
                class_name="flex-row items-center gap-2",
            ),
            class_name=(
                "relative flex-row items-center "
                "px-5 py-4 overflow-hidden bg-emerald-500/10 dark:bg-white/[0.03] "
                f"{_divider}"
            ),
        ),
        _share_row(
            "facebook",
            "Facebook",
            "https://www.facebook.com/sharer/sharer.php?u=https://nursereports.org&amp;src=sdkpreparse",
        ),
        _share_row(
            "twitter",
            "Twitter / X",
            "https://twitter.com/intent/post?text=Nationwide hospital reporting built by nurses for nurses.&url=https%3A%2F%2Fnursereports.org",
        ),
        _share_row(
            "linkedin",
            "LinkedIn",
            "https://www.linkedin.com/sharing/share-offsite/?url=https://nursereports.org",
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _dashboard_card() -> rx.Component:
    return rx.flex(
        button(
            icon("layout-dashboard", class_name="h-4 w-4"),
            "Go to Dashboard",
            variant="solid",
            on_click=rx.redirect("/dashboard"),
            width="full",
        ),
        class_name="flex-col",
    )


def _fireworks() -> rx.Component:
    return confetti(
        recycle=False,
        number_of_pieces=300,
        gravity=0.15,
    )
