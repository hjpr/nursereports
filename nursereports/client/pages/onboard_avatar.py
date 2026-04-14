from ..components import button, heading, icon, login_protected, text
from .navbar import navbar
from .footer import footer
from ...states import BaseState, OnboardState
from ...states.onboard_state import AVATARS

import reflex as rx


_CARD = (
    "flex-col "
    "bg-emerald-500/20 dark:bg-white/[0.03] "
    "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
    "rounded-2xl overflow-hidden"
)

_DIVIDER = "border-b border-neutral-300 dark:border-neutral-800/50"


@rx.page(
    route="/onboard/avatar",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        OnboardState.event_state_onboard_flow,
    ],
)
@login_protected
def onboard_avatar_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        rx.flex(
            _step_progress(2),
            _avatar_card(),
            class_name=(
                "flex-col gap-6 "
                "w-full max-w-screen-sm "
                "mx-auto px-4 pt-6 md:pt-10 pb-16"
            ),
        ),
        class_name="flex-1 flex-col items-center w-full",
    )


def _step_progress(active: int) -> rx.Component:
    _active = "h-1 flex-1 rounded-full bg-emerald-500"
    _inactive = "h-1 flex-1 rounded-full bg-neutral-200 dark:bg-neutral-800"
    labels = ["Welcome", "Identity", "Avatar", "Background"]
    return rx.flex(
        rx.flex(
            *[
                rx.box(class_name=_active if i <= active else _inactive)
                for i in range(4)
            ],
            class_name="flex-row gap-1.5 w-full",
        ),
        text(
            f"Step {active + 1} of 4 — {labels[active]}",
            size="xs",
            class_name="text-neutral-400 dark:text-neutral-500 mt-1",
        ),
        class_name="flex-col gap-1",
    )


def _card_header(icon_tag: str, title: str) -> rx.Component:
    return rx.flex(
        rx.box(class_name="absolute inset-0 pointer-events-none"),
        rx.flex(
            icon(icon_tag, accent=True, class_name="h-5 w-5 relative"),
            heading(title, size="sm", class_name="relative"),
            class_name="flex-row items-center gap-2",
        ),
        class_name=(
            f"relative flex-row items-center px-5 py-4 overflow-hidden "
            f"bg-emerald-500/10 dark:bg-white/[0.03] {_DIVIDER}"
        ),
    )


def _avatar_card() -> rx.Component:
    return rx.flex(
        _card_header("smile", "Choose Your Avatar"),
        rx.flex(
            *[_avatar_option(name) for name in AVATARS],
            class_name=f"grid grid-cols-3 gap-4 p-5 {_DIVIDER}",
        ),
        rx.flex(
            button(
                "Back",
                variant="outline",
                on_click=rx.redirect("/onboard/identity"),
            ),
            button(
                "Next",
                variant="solid",
                on_click=OnboardState.event_state_next_from_avatar,
            ),
            class_name="flex-row justify-between gap-3 px-5 py-4",
        ),
        class_name=_CARD,
    )


def _avatar_option(avatar_name: str) -> rx.Component:
    is_selected = OnboardState.selected_icon == avatar_name
    return rx.flex(
        rx.image(
            src=f"/raster/avatars/{avatar_name}.svg",
            width="52px",
            height="52px",
            class_name="rounded-full",
        ),
        on_click=OnboardState.set_selected_icon(avatar_name),
        class_name=rx.cond(
            is_selected,
            (
                "flex items-center justify-center p-3 "
                "rounded-2xl cursor-pointer "
                "ring-[3px] ring-emerald-500 "
                "bg-emerald-500/10 "
                "transition-all duration-150"
            ),
            (
                "flex items-center justify-center p-3 "
                "rounded-2xl cursor-pointer "
                "ring-[1.5px] ring-neutral-200 dark:ring-neutral-700 "
                "hover:ring-neutral-300 dark:hover:ring-neutral-600 "
                "hover:bg-neutral-50 dark:hover:bg-white/[0.03] "
                "transition-all duration-150"
            ),
        ),
    )
