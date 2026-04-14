from ..components import (
    button,
    heading,
    icon,
    login_protected,
    text,
)
from .navbar import navbar
from ...states import BaseState, ReportState

import reflex as rx


@rx.page(
    route="/report/[report_mode]/research",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def research_page() -> rx.Component:
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
        _edit_banner(),
        _step_progress(4),
        _campaign_card(),
        class_name=(
            "flex-col gap-4 "
            "w-full max-w-screen-sm "
            "mx-auto px-4 pt-4 md:pt-10 pb-10"
        ),
    )


# ---------------------------------------------------------------------------
# Shared helpers
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


def _edit_banner() -> rx.Component:
    return rx.cond(
        ReportState.mode == "edit",
        rx.flex(
            icon("pencil", accent=True, class_name="h-4 w-4 shrink-0"),
            text(
                "Editing a previously submitted report.",
                size="sm",
                class_name="text-neutral-600 dark:text-neutral-400",
            ),
            class_name=(
                "flex-row items-center gap-2 px-4 py-3 "
                "bg-emerald-500/10 dark:bg-white/[0.03] "
                "ring-[1.5px] ring-emerald-500/30 dark:ring-emerald-500/20 "
                "rounded-xl"
            ),
        ),
    )


def _step_progress(step: int) -> rx.Component:
    labels = {1: "Compensation", 2: "Assignment", 3: "Staffing", 4: "Research"}
    segments = [
        rx.box(
            class_name=(
                "h-1 flex-1 rounded-full bg-emerald-500"
                if i <= step
                else "h-1 flex-1 rounded-full bg-neutral-200 dark:bg-neutral-800"
            ),
        )
        for i in range(1, 5)
    ]
    return rx.flex(
        rx.flex(*segments, class_name="flex-row gap-1.5 w-full"),
        text(
            f"Step {step} of 4 — {labels[step]}",
            size="xs",
            class_name="text-neutral-400 dark:text-neutral-500 mt-1",
        ),
        class_name="flex-col gap-1",
    )


def _field_label(label: str, optional: bool = False) -> rx.Component:
    if optional:
        return rx.flex(
            text(label, size="sm", weight="medium"),
            text("Optional", size="xs", class_name="text-neutral-400 dark:text-neutral-500"),
            class_name="flex-row items-center justify-between",
        )
    return text(label, size="sm", weight="medium")


def _check_icon(condition) -> rx.Component:
    return rx.cond(
        condition,
        icon("circle-check-big", accent=True, class_name="h-5 w-5 shrink-0"),
        rx.icon("circle-alert", class_name="h-5 w-5 shrink-0 text-neutral-300 dark:text-neutral-700"),
    )


def _emoji_rating(score_var, setter) -> rx.Component:
    def _emoji(name: str, value: int, active_cls: str) -> rx.Component:
        return rx.flex(
            rx.cond(
                score_var == value,
                rx.icon(name, class_name=f"h-10 w-10 stroke-[1.5] {active_cls}"),
                rx.icon(name, class_name="h-10 w-10 stroke-[1.5] stroke-neutral-300 dark:stroke-neutral-700"),
            ),
            on_click=setter(value),
            class_name=(
                "p-3 cursor-pointer rounded-xl "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800/60 "
                "transition-colors duration-150"
            ),
        )

    return rx.flex(
        _emoji("angry", 1, "fill-rose-400 stroke-rose-500"),
        _emoji("frown", 2, "fill-orange-400 stroke-orange-500"),
        _emoji("meh", 3, "fill-amber-300 stroke-amber-400"),
        _emoji("smile", 4, "fill-emerald-400 stroke-emerald-500"),
        _emoji("laugh", 5, "fill-sky-400 stroke-sky-500"),
        class_name="flex-row justify-around w-full py-1",
    )


# ---------------------------------------------------------------------------
# Campaign Card
# ---------------------------------------------------------------------------

def _campaign_card() -> rx.Component:
    return rx.flex(
        _card_header("flask-conical", "Research Questions"),
        # Intro blurb
        rx.flex(
            text(
                "Help us understand the broader nursing landscape. "
                "Your answers are used to surface trends and advocate for nurses nationwide.",
                size="sm",
                class_name="text-neutral-600 dark:text-neutral-400",
            ),
            class_name="flex-col px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Q1 — Leaving
        rx.flex(
            rx.flex(
                _field_label("Are you considering leaving your current nursing position in the next 12 months?"),
                _check_icon(ReportState.research_select_leaving),
                class_name="flex-row items-center justify-between",
            ),
            rx.select(
                ["Yes", "No"],
                placeholder="— Select —",
                value=ReportState.research_select_leaving,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_research_select_leaving,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Q2 — Mental health support
        rx.flex(
            rx.flex(
                _field_label("Do you feel your hospital adequately supports nurse mental health?"),
                _check_icon(ReportState.research_select_mental_health),
                class_name="flex-row items-center justify-between",
            ),
            rx.select(
                ["Yes", "No"],
                placeholder="— Select —",
                value=ReportState.research_select_mental_health,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_research_select_mental_health,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Q3 — Career satisfaction emoji rating
        rx.flex(
            rx.flex(
                _field_label("Overall, how satisfied are you with nursing as a career?"),
                _check_icon(ReportState.research_select_career_rating),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(
                ReportState.research_select_career_rating,
                ReportState.set_research_select_career_rating,
            ),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Q4 — Open comment (optional)
        rx.flex(
            _field_label("Anything else you'd like to share with us?", optional=True),
            rx.debounce_input(
                rx.text_area(
                    value=ReportState.research_input_comments,
                    placeholder="Do not enter personally identifiable information.",
                    color_scheme="green",
                    on_change=ReportState.set_research_input_comments,
                    on_blur=ReportState.set_research_input_comments,
                    size="3",
                    rows="4",
                    width="100%",
                ),
                debounce_timeout=1000,
            ),
            rx.cond(
                ReportState.research_input_comments,
                rx.cond(
                    ReportState.research_input_comments_chars_left < 0,
                    text(
                        "Over 500 character limit.",
                        size="xs",
                        class_name="text-rose-500 dark:text-rose-400",
                    ),
                    text(
                        f"{ReportState.research_input_comments_chars_left} chars left",
                        size="xs",
                        class_name="text-neutral-400 dark:text-neutral-500",
                    ),
                ),
                text(
                    "500 character limit.",
                    size="xs",
                    class_name="text-neutral-400 dark:text-neutral-500",
                ),
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Navigation
        rx.cond(
            ReportState.user_is_loading,
            rx.flex(
                rx.icon("loader-circle", class_name="animate-spin h-5 w-5 text-neutral-400"),
                class_name="flex-row items-center justify-center px-5 py-4",
            ),
            rx.flex(
                button(
                    "Back",
                    variant="outline",
                    on_click=rx.redirect(f"/report/{ReportState.mode}/staffing"),
                ),
                rx.cond(
                    ReportState.mode == "edit",
                    button(
                        "Submit Edits",
                        variant="solid",
                        on_click=[
                            ReportState.set_user_is_loading(True),
                            ReportState.handle_submit_research,
                        ],
                    ),
                    button(
                        "Submit Report",
                        variant="solid",
                        on_click=[
                            ReportState.set_user_is_loading(True),
                            ReportState.handle_submit_research,
                        ],
                    ),
                ),
                class_name="flex-row justify-between gap-3 px-5 py-4",
            ),
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )
