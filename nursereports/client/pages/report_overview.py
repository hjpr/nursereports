from ..components import (
    button,
    heading,
    icon,
    login_protected,
    text,
)
from .navbar import navbar
from ...states import BaseState, ReportState, UserState

import reflex as rx


@rx.page(
    route="/report/[report_mode]/overview",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def overview_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        class_name=(
            "flex-col items-center "
            "bg-neutral-50 dark:bg-[#07100a] "
            "min-h-screen w-full"
        ),
    )


def _content() -> rx.Component:
    return rx.flex(
        _hospital_card(),
        class_name=(
            "flex-col gap-4 "
            "w-full max-w-screen-sm "
            "mx-auto px-4 pt-4 md:pt-10 pb-10"
        ),
    )


# ---------------------------------------------------------------------------
# Card header helper
# ---------------------------------------------------------------------------

def _card_header(icon_tag: str, title: str) -> rx.Component:
    return rx.flex(
        rx.box(class_name="absolute inset-0 pointer-events-none"),
        rx.flex(
            icon(icon_tag, accent=True, class_name="h-5 w-5 relative"),
            heading(title, size="sm", class_name="relative"),
            class_name="flex-row items-center gap-2",
        ),
        class_name=(
            "relative flex-row items-center "
            "px-5 py-4 overflow-hidden bg-emerald-500/10 dark:bg-white/[0.03] "
            "border-b border-neutral-300 dark:border-neutral-800/50"
        ),
    )


# ---------------------------------------------------------------------------
# Hospital overview card
# ---------------------------------------------------------------------------

def _hospital_card() -> rx.Component:
    return rx.flex(
        _card_header(
            "file-text",
            rx.match(
                ReportState.mode,
                ("edit", "Editing Report"),
                ("full-report", "Submitting Full Report"),
                ("pay-report", "Submitting Pay Report"),
                ("red-flag", "Red Flag Report"),
                "Submit Report",
            ),
        ),
        # Hospital identity
        rx.flex(
            rx.skeleton(
                heading(
                    ReportState.hospital_info["hosp_name"],
                    size="lg",
                    class_name="relative",
                ),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                text(
                    ReportState.hospital_info["hosp_addr"],
                    class_name="relative text-neutral-500 dark:text-neutral-400 mt-0.5",
                ),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                text(
                    ReportState.hospital_info["hosp_city"],
                    ", ",
                    ReportState.hospital_info["hosp_state"],
                    " ",
                    ReportState.hospital_info["hosp_zip"],
                    class_name="relative text-neutral-500 dark:text-neutral-400",
                ),
                loading=~rx.State.is_hydrated,
            ),
            class_name="flex-col relative px-5 py-6 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Info rows
        _info_row(
            "eye-off",
            "All reporting is anonymous. No details are attached to your report beyond what you choose to share.",
        ),
        _info_row(
            "stethoscope",
            "We're not associated with corporate interests. Your report helps a fellow nurse make a more informed decision about where to work.",
        ),
        _info_row(
            "clock",
            "Your time is valuable. This should only take about 5-7 minutes.",
        ),
        # Navigation
        rx.flex(
            rx.cond(
                ReportState.mode == "edit",
                button(
                    "Back",
                    variant="outline",
                    on_click=rx.redirect("/dashboard"),
                ),
                rx.cond(
                    UserState.user_needs_onboarding,
                    button(
                        "Back",
                        variant="outline",
                        on_click=rx.redirect("/search/hospital"),
                    ),
                    button(
                        "Back",
                        variant="outline",
                        on_click=rx.redirect(f"/hospital/{ReportState.hospital_id}"),
                    ),
                ),
            ),
            button(
                "Next",
                variant="solid",
                on_click=rx.redirect(f"/report/{ReportState.mode}/compensation"),
            ),
            class_name="flex-row justify-between gap-3 px-5 py-4",
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _info_row(icon_tag: str, message: str) -> rx.Component:
    return rx.flex(
        icon(icon_tag, accent=True, class_name="h-5 w-5 shrink-0 mt-0.5"),
        text(message, size="sm", class_name="text-neutral-600 dark:text-neutral-400"),
        class_name="flex-row items-start gap-4 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
    )
