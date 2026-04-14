from ..components import button, heading, icon, login_protected, text
from .navbar import navbar
from .footer import footer
from ...states import BaseState, OnboardState, SearchState

import reflex as rx


_CARD = (
    "flex-col "
    "bg-emerald-500/20 dark:bg-white/[0.03] "
    "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
    "rounded-2xl overflow-hidden"
)

_DIVIDER = "border-b border-neutral-300 dark:border-neutral-800/50"


@rx.page(
    route="/onboard/background",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        OnboardState.event_state_onboard_flow,
    ],
)
@login_protected
def onboard_background_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        rx.flex(
            _step_progress(3),
            _background_card(),
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


def _check_icon(condition) -> rx.Component:
    return rx.cond(
        condition,
        icon("circle-check-big", accent=True, class_name="h-5 w-5 shrink-0"),
        rx.icon(
            "circle-alert",
            class_name="h-5 w-5 shrink-0 text-neutral-300 dark:text-neutral-700",
        ),
    )


def _field_label(label: str) -> rx.Component:
    return text(label, size="sm", weight="medium")


def _background_card() -> rx.Component:
    return rx.flex(
        _card_header("stethoscope", "Nursing Information"),
        # License type
        rx.flex(
            rx.flex(
                _field_label("What is your license?"),
                _check_icon(OnboardState.license),
                class_name="flex-row items-center justify-between w-full",
            ),
            rx.select(
                [
                    "APRN",
                    "RN - Bachelors",
                    "RN - Associates",
                    "LPN/LVN",
                    "Nursing Student",
                ],
                placeholder="- Select one -",
                value=OnboardState.license,
                position="popper",
                on_change=OnboardState.set_license,
                required=True,
                size="3",
                width="100%",
            ),
            class_name=f"flex-col gap-2 px-5 py-4 {_DIVIDER}",
        ),
        # License state
        rx.flex(
            rx.flex(
                rx.cond(
                    OnboardState.license == "Nursing Student",
                    _field_label("What state do you attend school in?"),
                    _field_label("What state do you primarily practice in?"),
                ),
                _check_icon(OnboardState.license_state),
                class_name="flex-row items-center justify-between gap-3 w-full",
            ),
            rx.select(
                SearchState.state_options,
                placeholder="- Select one -",
                value=OnboardState.license_state,
                position="popper",
                on_change=OnboardState.set_license_state,
                required=True,
                size="3",
                width="100%",
            ),
            class_name=f"flex-col gap-2 px-5 py-4 {_DIVIDER}",
        ),
        # Hospital experience
        rx.flex(
            rx.flex(
                _field_label("Have you worked in a hospital in a nursing role within the past year?"),
                _check_icon(
                    (OnboardState.license == "Nursing Student") | OnboardState.has_review
                ),
                class_name="flex-row items-center justify-between gap-3 w-full",
            ),
            rx.select(
                ["Yes", "No"],
                placeholder="- Select one -",
                value=OnboardState.has_review,
                position="popper",
                on_change=OnboardState.set_has_review,
                required=True,
                disabled=(OnboardState.license == "Nursing Student"),
                size="3",
                width="100%",
            ),
            class_name=f"flex-col gap-2 px-5 py-4 {_DIVIDER}",
        ),
        # Callout when no report required
        rx.cond(
            (OnboardState.license == "Nursing Student")
            | (OnboardState.has_review == "No"),
            rx.flex(
                rx.callout(
                    "You won't be required to submit a report right now.",
                    icon="info",
                    class_name="w-full",
                ),
                class_name=f"px-5 py-4 {_DIVIDER}",
            ),
        ),
        # Nav
        rx.cond(
            OnboardState.user_is_loading,
            rx.flex(
                rx.icon("loader-circle", class_name="animate-spin h-5 w-5 text-neutral-400"),
                class_name="flex-row items-center justify-center px-5 py-4",
            ),
            rx.flex(
                button(
                    "Back",
                    variant="outline",
                    on_click=rx.redirect("/onboard/avatar"),
                ),
                button(
                    "Submit & Continue",
                    variant="solid",
                    on_click=[
                        OnboardState.set_user_is_loading(True),
                        OnboardState.event_state_submit_onboard,
                        OnboardState.set_user_is_loading(False),
                    ],
                ),
                class_name="flex-row justify-between gap-3 px-5 py-4",
            ),
        ),
        class_name=_CARD,
    )
