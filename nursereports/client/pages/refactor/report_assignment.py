from ...components import (
    button,
    heading,
    icon,
    login_protected,
    text,
)
from .navbar import navbar
from ....states import BaseState, ReportState, constants_types

import reflex as rx


@rx.page(
    route="/report/[report_mode]/assignment",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def assignment_page() -> rx.Component:
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
        _step_progress(2),
        _role_card(),
        _specialties_card(),
        _team_card(),
        _overall_card(),
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
    labels = {1: "Compensation", 2: "Assignment", 3: "Staffing"}
    segments = [
        rx.box(
            class_name=(
                "h-1 flex-1 rounded-full bg-emerald-500"
                if i <= step
                else "h-1 flex-1 rounded-full bg-neutral-200 dark:bg-neutral-800"
            ),
        )
        for i in range(1, 4)
    ]
    return rx.flex(
        rx.flex(*segments, class_name="flex-row gap-1.5 w-full"),
        text(
            f"Step {step} of 3 — {labels[step]}",
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


def _comments_field(value, setter, chars_left) -> rx.Component:
    return rx.flex(
        _field_label("Comments for your nursing peers", optional=True),
        rx.debounce_input(
            rx.text_area(
                value=value,
                placeholder="Do not enter personally identifiable information.",
                color_scheme="green",
                on_change=setter,
                on_blur=setter,
                size="3",
                rows="4",
                width="100%",
            ),
            debounce_timeout=1000,
        ),
        rx.cond(
            value,
            rx.cond(
                chars_left < 0,
                text(
                    "Over 1000 character limit.",
                    size="xs",
                    class_name="text-rose-500 dark:text-rose-400",
                ),
                text(
                    f"{chars_left} chars left",
                    size="xs",
                    class_name="text-neutral-400 dark:text-neutral-500",
                ),
            ),
            text(
                "1000 character limit.",
                size="xs",
                class_name="text-neutral-400 dark:text-neutral-500",
            ),
        ),
        class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
    )


# ---------------------------------------------------------------------------
# Card 1 — Your Role
# ---------------------------------------------------------------------------

def _role_card() -> rx.Component:
    return rx.flex(
        _card_header("stethoscope", "Your Role"),
        # Work classification
        rx.flex(
            rx.flex(
                _field_label("How would you classify where you work?"),
                _check_icon(ReportState.assign_select_classify),
                class_name="flex-row items-center justify-between",
            ),
            rx.flex(
                text("Unit — STICU, PACU, 6 NORTH, ED", size="xs", class_name="text-neutral-500"),
                text("Area — OR, VIR, CATH LAB", size="xs", class_name="text-neutral-500"),
                text("Role — WOUND CARE, ICU TRANSPORT, FLOAT POOL", size="xs", class_name="text-neutral-500"),
                class_name="flex-col gap-0.5",
            ),
            rx.select(
                constants_types.ASSIGN_SELECT_CLASSIFY_SELECTIONS,
                placeholder="— Select —",
                value=ReportState.assign_select_classify,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_assign_select_classify,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Conditional branch: Unit / Area / Role
        rx.match(
            ReportState.assign_select_classify,
            (
                "Unit",
                rx.flex(
                    # Unit select
                    rx.flex(
                        rx.flex(
                            _field_label("What unit are you submitting a report for?"),
                            _check_icon(ReportState.assign_select_unit),
                            class_name="flex-row items-center justify-between",
                        ),
                        rx.select(
                            ReportState.hospital_units,
                            placeholder="— Select —",
                            value=ReportState.assign_select_unit,
                            position="popper",
                            color_scheme="green",
                            on_change=ReportState.set_assign_select_unit,
                            size="3",
                            width="100%",
                        ),
                        class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
                    ),
                    # Custom unit name (conditional)
                    rx.cond(
                        ReportState.assign_select_unit == "I don't see my unit",
                        rx.flex(
                            rx.flex(
                                _field_label("Enter your unit as it's commonly known."),
                                _check_icon(ReportState.assign_input_unit),
                                class_name="flex-row items-center justify-between",
                            ),
                            rx.debounce_input(
                                rx.input(
                                    value=ReportState.assign_input_unit,
                                    placeholder="e.g. MICU, 4 WEST",
                                    on_change=ReportState.set_assign_input_unit,
                                    color_scheme="green",
                                    size="3",
                                    max_length=50,
                                    width="100%",
                                ),
                                debounce_timeout=600,
                            ),
                            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
                        ),
                    ),
                    # Acuity
                    rx.flex(
                        rx.flex(
                            _field_label("What is the acuity of your unit?"),
                            _check_icon(ReportState.assign_select_acuity),
                            class_name="flex-row items-center justify-between",
                        ),
                        rx.select(
                            constants_types.ASSIGN_SELECT_ACUITY_SELECTIONS,
                            placeholder="— Select —",
                            value=ReportState.assign_select_acuity,
                            position="popper",
                            color_scheme="green",
                            on_change=ReportState.set_assign_select_acuity,
                            size="3",
                            width="100%",
                        ),
                        class_name="flex-col gap-3 px-5 py-4",
                    ),
                    class_name="flex-col w-full",
                ),
            ),
            (
                "Area",
                rx.flex(
                    rx.flex(
                        rx.flex(
                            _field_label("What area are you submitting a report for?"),
                            _check_icon(ReportState.assign_select_area),
                            class_name="flex-row items-center justify-between",
                        ),
                        rx.select(
                            ReportState.hospital_areas,
                            placeholder="— Select —",
                            value=ReportState.assign_select_area,
                            position="popper",
                            color_scheme="green",
                            on_change=ReportState.set_assign_select_area,
                            size="3",
                            width="100%",
                        ),
                        class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
                    ),
                    rx.cond(
                        ReportState.assign_select_area == "I don't see my area",
                        rx.flex(
                            rx.flex(
                                _field_label("Enter your area as it's commonly known."),
                                _check_icon(ReportState.assign_input_area),
                                class_name="flex-row items-center justify-between",
                            ),
                            rx.debounce_input(
                                rx.input(
                                    value=ReportState.assign_input_area,
                                    placeholder="e.g. OR, CATH LAB",
                                    on_change=ReportState.set_assign_input_area,
                                    color_scheme="green",
                                    size="3",
                                    max_length=50,
                                    width="100%",
                                ),
                                debounce_timeout=600,
                            ),
                            class_name="flex-col gap-3 px-5 py-4",
                        ),
                    ),
                    class_name="flex-col w-full",
                ),
            ),
            (
                "Role",
                rx.flex(
                    rx.flex(
                        rx.flex(
                            _field_label("What role are you submitting a report for?"),
                            _check_icon(ReportState.assign_select_role),
                            class_name="flex-row items-center justify-between",
                        ),
                        rx.select(
                            ReportState.hospital_roles,
                            placeholder="— Select —",
                            value=ReportState.assign_select_role,
                            position="popper",
                            color_scheme="green",
                            on_change=ReportState.set_assign_select_role,
                            size="3",
                            width="100%",
                        ),
                        class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
                    ),
                    rx.cond(
                        ReportState.assign_select_role == "I don't see my role",
                        rx.flex(
                            rx.flex(
                                _field_label("Enter your role as it's commonly known."),
                                _check_icon(ReportState.assign_input_role),
                                class_name="flex-row items-center justify-between",
                            ),
                            rx.debounce_input(
                                rx.input(
                                    value=ReportState.assign_input_role,
                                    placeholder="e.g. FLOAT POOL, WOUND CARE",
                                    on_change=ReportState.set_assign_input_role,
                                    color_scheme="green",
                                    size="3",
                                    max_length=50,
                                    width="100%",
                                ),
                                debounce_timeout=600,
                            ),
                            class_name="flex-col gap-3 px-5 py-4",
                        ),
                    ),
                    class_name="flex-col w-full",
                ),
            ),
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Card 2 — Specialties
# ---------------------------------------------------------------------------

def _specialties_card() -> rx.Component:
    return rx.flex(
        _card_header("award", "Specialties"),
        rx.flex(
            _field_label("Select up to three specialties for your position.", optional=True),
            rx.select(
                ReportState.assign_specialty_1,
                placeholder="— Specialty 1 —",
                value=ReportState.assign_select_specialty_1,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_assign_select_specialty_1,
                size="3",
                width="100%",
            ),
            rx.select(
                ReportState.assign_specialty_2,
                placeholder="— Specialty 2 —",
                value=ReportState.assign_select_specialty_2,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_assign_select_specialty_2,
                disabled=~ReportState.assign_select_specialty_1,
                size="3",
                width="100%",
            ),
            rx.select(
                ReportState.assign_specialty_3,
                placeholder="— Specialty 3 —",
                value=ReportState.assign_select_specialty_3,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_assign_select_specialty_3,
                disabled=~ReportState.assign_select_specialty_2,
                size="3",
                width="100%",
            ),
            rx.cond(
                ReportState.assign_select_specialty_1,
                button(
                    "Clear",
                    variant="ghost",
                    size="sm",
                    on_click=[
                        ReportState.set_assign_select_specialty_1(""),
                        ReportState.set_assign_select_specialty_2(""),
                        ReportState.set_assign_select_specialty_3(""),
                    ],
                ),
            ),
            class_name="flex-col gap-3 px-5 py-4",
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Card 3 — Team & Culture
# ---------------------------------------------------------------------------

def _team_card() -> rx.Component:
    return rx.flex(
        _card_header("users", "Team & Culture"),
        # Rate nurses
        rx.flex(
            rx.flex(
                _field_label("How is working with the nurses around you?"),
                _check_icon(ReportState.assign_select_rate_nurses),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.assign_select_rate_nurses, ReportState.set_assign_select_rate_nurses),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Rate nurse aides
        rx.flex(
            rx.flex(
                _field_label("How is working with the nurse aides around you?"),
                _check_icon(ReportState.assign_select_rate_nurse_aides),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.assign_select_rate_nurse_aides, ReportState.set_assign_select_rate_nurse_aides),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Rate physicians
        rx.flex(
            rx.flex(
                _field_label("How is working with the physicians around you?"),
                _check_icon(ReportState.assign_select_rate_physicians),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.assign_select_rate_physicians, ReportState.set_assign_select_rate_physicians),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Rate management
        rx.flex(
            rx.flex(
                _field_label("How is working with management?"),
                _check_icon(ReportState.assign_select_rate_management),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.assign_select_rate_management, ReportState.set_assign_select_rate_management),
            class_name="flex-col gap-2 px-5 py-4",
        ),
        class_name=(
            "flex-col "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Card 4 — Overall
# ---------------------------------------------------------------------------

def _overall_card() -> rx.Component:
    return rx.flex(
        _card_header("star", "Overall"),
        # Recommend
        rx.flex(
            rx.flex(
                _field_label("Would you recommend this assignment to other nurses?"),
                _check_icon(ReportState.assign_select_recommend),
                class_name="flex-row items-center justify-between",
            ),
            rx.select(
                constants_types.ASSIGN_SELECT_RECOMMEND_SELECTIONS,
                placeholder="— Select —",
                value=ReportState.assign_select_recommend,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_assign_select_recommend,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Overall rating
        rx.flex(
            rx.flex(
                _field_label("Rate your assignment overall."),
                _check_icon(ReportState.assign_select_overall),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.assign_select_overall, ReportState.set_assign_select_overall),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Comments
        _comments_field(
            ReportState.assign_input_comments,
            ReportState.set_assign_input_comments,
            ReportState.assign_input_comments_chars_left,
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
                    on_click=rx.redirect(f"/report/{ReportState.mode}/compensation"),
                ),
                button(
                    "Next",
                    variant="solid",
                    on_click=[
                        ReportState.set_user_is_loading(True),
                        ReportState.handle_submit_assignment,
                        ReportState.set_user_is_loading(False),
                    ],
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
