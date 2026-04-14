from ..components import button, heading, icon, login_protected, text
from .navbar import navbar
from .footer import footer
from ...states import BaseState, OnboardState

import reflex as rx


_SLIDE_STYLE = """
<style>
@keyframes slide-in-from-right {
  from { transform: translateX(40px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}
@keyframes slide-in-from-left {
  from { transform: translateX(-40px); opacity: 0; }
  to   { transform: translateX(0);     opacity: 1; }
}
.name-slide-right { animation: slide-in-from-right 0.22s ease-out both; }
.name-slide-left  { animation: slide-in-from-left  0.22s ease-out both; }
</style>
"""

_CARD = (
    "flex-col "
    "bg-emerald-500/20 dark:bg-white/[0.03] "
    "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
    "rounded-2xl overflow-hidden"
)

_DIVIDER = "border-b border-neutral-300 dark:border-neutral-800/50"


@rx.page(
    route="/onboard/identity",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        OnboardState.event_state_onboard_flow,
        OnboardState.event_state_generate_display_name,
    ],
)
@login_protected
def onboard_identity_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        rx.html(_SLIDE_STYLE),
        rx.flex(
            _step_progress(1),
            _identity_card(),
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


def _identity_card() -> rx.Component:
    return rx.flex(
        _card_header("user-round", "Your Anonymous Identity"),
        # Carousel row
        rx.flex(
            # Back arrow
            rx.flex(
                rx.cond(
                    OnboardState.can_go_back,
                    rx.icon(
                        "chevron-left",
                        class_name=(
                            "h-5 w-5 cursor-pointer "
                            "text-neutral-500 hover:text-emerald-600 "
                            "dark:text-neutral-400 dark:hover:text-emerald-500 "
                            "transition-colors duration-150"
                        ),
                        on_click=OnboardState.event_state_name_prev,
                    ),
                    rx.icon(
                        "chevron-left",
                        class_name="h-5 w-5 text-neutral-300 dark:text-neutral-700",
                    ),
                ),
                class_name="flex items-center justify-center w-10 shrink-0",
            ),
            # Name — overflow-hidden clips the slide animation
            rx.flex(
                rx.el.div(
                    rx.text(
                        OnboardState.display_name,
                        class_name=(
                            "font-mono text-lg font-semibold text-center "
                            "text-emerald-600 dark:text-emerald-500 break-all"
                        ),
                    ),
                    key=OnboardState.name_key,
                    class_name=rx.cond(
                        OnboardState.slide_direction == "right",
                        "name-slide-right w-full",
                        "name-slide-left w-full",
                    ),
                ),
                class_name="flex-1 overflow-hidden flex items-center justify-center py-6",
            ),
            # Forward arrow
            rx.flex(
                rx.cond(
                    OnboardState.can_go_forward,
                    rx.icon(
                        "chevron-right",
                        class_name=(
                            "h-5 w-5 cursor-pointer "
                            "text-neutral-500 hover:text-emerald-600 "
                            "dark:text-neutral-400 dark:hover:text-emerald-500 "
                            "transition-colors duration-150"
                        ),
                        on_click=OnboardState.event_state_name_next,
                    ),
                    rx.icon(
                        "chevron-right",
                        class_name="h-5 w-5 text-neutral-300 dark:text-neutral-700",
                    ),
                ),
                class_name="flex items-center justify-center w-10 shrink-0",
            ),
            class_name=f"flex-row items-center px-2 {_DIVIDER}",
        ),
        # Blip indicators
        rx.flex(
            *[
                rx.box(
                    class_name=rx.cond(
                        OnboardState.name_index == i,
                        "w-4 h-1.5 rounded-full bg-emerald-500 transition-all duration-200",
                        "w-1.5 h-1.5 rounded-full bg-neutral-300 dark:bg-neutral-700 transition-all duration-200",
                    ),
                )
                for i in range(6)
            ],
            class_name=f"flex-row items-center justify-center gap-1.5 py-3 {_DIVIDER}",
        ),
        # Nav
        rx.flex(
            button(
                "Back",
                variant="outline",
                on_click=rx.redirect("/onboard/welcome"),
            ),
            button(
                "Next",
                variant="solid",
                on_click=OnboardState.event_state_next_from_identity,
            ),
            class_name="flex-row justify-between gap-3 px-5 py-4",
        ),
        class_name=_CARD,
    )
