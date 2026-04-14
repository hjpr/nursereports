from ..components import (
    button,
    heading,
    icon,
    login_protected,
    text,
)
from .navbar import navbar
from ...states import BaseState, ReportState, constants_types

import reflex as rx


@rx.page(
    route="/report/[report_mode]/staffing",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_login,
        ReportState.event_state_report_flow,
    ],
)
@login_protected
def staffing_page() -> rx.Component:
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
        _step_progress(3),
        _ratios_card(),
        _workload_card(),
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


def _chip(label: str, checked_var, toggle_handler) -> rx.Component:
    return rx.flex(
        rx.text(label, class_name="text-sm font-medium"),
        on_click=toggle_handler,
        class_name=rx.cond(
            checked_var,
            (
                "px-3 py-1.5 rounded-full cursor-pointer select-none "
                "bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 "
                "ring-[1.5px] ring-emerald-500/40 dark:ring-emerald-500/30"
            ),
            (
                "px-3 py-1.5 rounded-full cursor-pointer select-none "
                "bg-neutral-100 dark:bg-neutral-800/60 "
                "text-neutral-600 dark:text-neutral-400 "
                "ring-[1.5px] ring-neutral-300 dark:ring-neutral-700"
            ),
        ),
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


def _ratio_calc(label: str) -> rx.Component:
    _btn = (
        "flex-1 flex-col items-center justify-center "
        "ring-[1.5px] ring-neutral-300 dark:ring-neutral-700 rounded-lg "
        "p-3 cursor-pointer select-none "
        "active:bg-neutral-100 dark:active:bg-neutral-800 "
        "transition-colors duration-75"
    )

    def _digit(d: str) -> rx.Component:
        return rx.flex(
            rx.text(d, class_name="px-2 text-xl font-medium"),
            on_click=ReportState.set_calculator_ratio_value(d),
            class_name=_btn,
        )

    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                icon("pencil", muted=True, class_name="h-4 w-4"),
                on_click=[
                    ReportState.set_calculator_toggle_ratio(label),
                    ReportState.set_calculator_ratio_value("clear"),
                ],
                class_name=(
                    "p-2 cursor-pointer rounded-lg "
                    "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                    "transition-colors duration-150"
                ),
            )
        ),
        rx.popover.content(
            rx.flex(
                rx.flex(
                    rx.text(
                        f"{ReportState.calculator_ratio_value}",
                        class_name="text-4xl font-bold font-mono flex-1 text-right",
                    ),
                    class_name="flex-row items-baseline gap-2 py-3 border-b border-neutral-200 dark:border-neutral-800 mb-3",
                ),
                rx.flex(_digit("1"), _digit("2"), _digit("3"), class_name="flex-row gap-2 w-full"),
                rx.flex(_digit("4"), _digit("5"), _digit("6"), class_name="flex-row gap-2 w-full"),
                rx.flex(_digit("7"), _digit("8"), _digit("9"), class_name="flex-row gap-2 w-full"),
                rx.flex(
                    _digit("0"),
                    rx.flex(
                        icon("delete", muted=True, class_name="h-4 w-4"),
                        on_click=ReportState.set_calculator_ratio_value("clear"),
                        class_name=f"{_btn} flex-1",
                    ),
                    class_name="flex-row gap-2 w-full",
                ),
                rx.flex(
                    rx.popover.close(
                        rx.flex(
                            rx.text("Enter", class_name="font-bold text-emerald-600 dark:text-emerald-500"),
                            on_click=ReportState.set_calculator_ratio_value("enter"),
                            class_name=(
                                "flex-col items-center justify-center "
                                "ring-[1.5px] ring-emerald-500/40 dark:ring-emerald-500/30 rounded-lg "
                                "p-3 cursor-pointer select-none w-full "
                                "active:bg-neutral-100 dark:active:bg-neutral-800 "
                                "transition-colors duration-75"
                            ),
                        ),
                        class_name="w-full",
                    ),
                    class_name="flex-row w-full",
                ),
                class_name="flex-col gap-2 w-full max-w-xs",
            )
        ),
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
# Card 1 — Patient Ratios
# ---------------------------------------------------------------------------

def _ratios_card() -> rx.Component:
    return rx.flex(
        _card_header("users", "Patient Ratios"),
        # Has ratios
        rx.flex(
            rx.flex(
                _field_label("Does your assignment have patient ratios?"),
                _check_icon(ReportState.staffing_select_ratio),
                class_name="flex-row items-center justify-between",
            ),
            rx.select(
                constants_types.STAFFING_SELECT_RATIO_SELECTIONS,
                placeholder="— Select —",
                value=ReportState.staffing_select_ratio,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_staffing_select_ratio,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Actual ratio (conditional on Yes)
        rx.cond(
            ReportState.staffing_select_ratio == "Yes",
            rx.flex(
                rx.flex(
                    _field_label("What is your average nurse : patient ratio?"),
                    _check_icon(ReportState.staffing_input_actual_ratio),
                    class_name="flex-row items-center justify-between",
                ),
                rx.flex(
                    rx.cond(
                        ReportState.staffing_input_actual_ratio,
                        rx.text(
                            f"1 : {ReportState.staffing_input_actual_ratio}",
                            class_name="text-2xl font-bold font-mono tracking-tight",
                        ),
                        rx.text(
                            "1 : ?",
                            class_name="text-2xl font-bold font-mono tracking-tight text-neutral-400 dark:text-neutral-600",
                        ),
                    ),
                    _ratio_calc("actual_ratio"),
                    class_name="flex-row items-center gap-3",
                ),
                class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
            ),
        ),
        # Is ratio appropriate (conditional on Yes)
        rx.cond(
            ReportState.staffing_select_ratio == "Yes",
            rx.flex(
                rx.flex(
                    _field_label("Do you feel this ratio is safe and appropriate?"),
                    _check_icon(ReportState.staffing_select_ratio_appropriate),
                    class_name="flex-row items-center justify-between",
                ),
                rx.select(
                    constants_types.STAFFING_SELECT_RATIO_APPROPRIATE,
                    placeholder="— Select —",
                    value=ReportState.staffing_select_ratio_appropriate,
                    position="popper",
                    color_scheme="green",
                    on_change=ReportState.set_staffing_select_ratio_appropriate,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
            ),
        ),
        # Ideal ratio (conditional on Not appropriate)
        rx.cond(
            ReportState.staffing_select_ratio_appropriate == "No",
            rx.flex(
                rx.flex(
                    _field_label("What nurse : patient ratio would be safe?"),
                    _check_icon(ReportState.staffing_input_ideal_ratio),
                    class_name="flex-row items-center justify-between",
                ),
                rx.flex(
                    rx.cond(
                        ReportState.staffing_input_ideal_ratio,
                        rx.text(
                            f"1 : {ReportState.staffing_input_ideal_ratio}",
                            class_name="text-2xl font-bold font-mono tracking-tight",
                        ),
                        rx.text(
                            "1 : ?",
                            class_name="text-2xl font-bold font-mono tracking-tight text-neutral-400 dark:text-neutral-600",
                        ),
                    ),
                    _ratio_calc("ideal_ratio"),
                    class_name="flex-row items-center gap-3",
                ),
                class_name="flex-col gap-3 px-5 py-4",
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
# Card 2 — Workload & Support
# ---------------------------------------------------------------------------

def _workload_card() -> rx.Component:
    return rx.flex(
        _card_header("activity", "Workload & Support"),
        # Daily workload
        rx.flex(
            rx.flex(
                _field_label("How would you rate the average daily workload?"),
                _check_icon(ReportState.staffing_select_workload),
                class_name="flex-row items-center justify-between",
            ),
            rx.select(
                constants_types.STAFFING_SELECT_WORKLOAD_SELECTIONS,
                placeholder="— Select —",
                value=ReportState.staffing_select_workload,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_staffing_select_workload,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Shift-end feeling
        rx.flex(
            rx.flex(
                _field_label("How do you usually feel at the end of your shift?"),
                _check_icon(ReportState.staffing_select_rate_workload),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.staffing_select_rate_workload, ReportState.set_staffing_select_rate_workload),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Charge nurse present
        rx.flex(
            rx.flex(
                _field_label("Does your assignment have a charge nurse?"),
                _check_icon(ReportState.staffing_select_charge_present),
                class_name="flex-row items-center justify-between",
            ),
            rx.select(
                constants_types.STAFFING_SELECT_CHARGE_PRESENT_SELECTIONS,
                placeholder="— Select —",
                value=ReportState.staffing_select_charge_present,
                position="popper",
                color_scheme="green",
                on_change=ReportState.set_staffing_select_charge_present,
                size="3",
                width="100%",
            ),
            class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Charge takes patients (conditional)
        rx.cond(
            ReportState.staffing_select_charge_present == "Yes",
            rx.flex(
                rx.flex(
                    _field_label("Does your charge nurse have to take patients?"),
                    _check_icon(ReportState.staffing_select_charge_assignment),
                    class_name="flex-row items-center justify-between",
                ),
                rx.select(
                    constants_types.STAFFING_SELECT_CHARGE_ASSIGNMENT_SELECTIONS,
                    placeholder="— Select —",
                    value=ReportState.staffing_select_charge_assignment,
                    position="popper",
                    color_scheme="green",
                    on_change=ReportState.set_staffing_select_charge_assignment,
                    size="3",
                    width="100%",
                ),
                class_name="flex-col gap-3 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
            ),
        ),
        # Support staff chips
        rx.flex(
            _field_label("Support staff available as a resource", optional=True),
            rx.flex(
                _chip(
                    "Rapid Response",
                    ReportState.staffing_check_rapid_response,
                    ReportState.set_staffing_check_rapid_response(~ReportState.staffing_check_rapid_response),
                ),
                _chip(
                    "Behavioral Response",
                    ReportState.staffing_check_behavioral_response,
                    ReportState.set_staffing_check_behavioral_response(~ReportState.staffing_check_behavioral_response),
                ),
                _chip(
                    "Transport",
                    ReportState.staffing_check_transport,
                    ReportState.set_staffing_check_transport(~ReportState.staffing_check_transport),
                ),
                _chip(
                    "Phlebotomy",
                    ReportState.staffing_check_phlebotomy,
                    ReportState.set_staffing_check_phlebotomy(~ReportState.staffing_check_phlebotomy),
                ),
                _chip(
                    "CVAD",
                    ReportState.staffing_check_cvad,
                    ReportState.set_staffing_check_cvad(~ReportState.staffing_check_cvad),
                ),
                _chip(
                    "IV Team",
                    ReportState.staffing_check_ivt,
                    ReportState.set_staffing_check_ivt(~ReportState.staffing_check_ivt),
                ),
                _chip(
                    "Wound Care",
                    ReportState.staffing_check_wocn,
                    ReportState.set_staffing_check_wocn(~ReportState.staffing_check_wocn),
                ),
                _chip(
                    "Chaplain",
                    ReportState.staffing_check_chaplain,
                    ReportState.set_staffing_check_chaplain(~ReportState.staffing_check_chaplain),
                ),
                _chip(
                    "Educator",
                    ReportState.staffing_check_educator,
                    ReportState.set_staffing_check_educator(~ReportState.staffing_check_educator),
                ),
                class_name="flex-row flex-wrap gap-2",
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
# Card 3 — Overall
# ---------------------------------------------------------------------------

def _overall_card() -> rx.Component:
    return rx.flex(
        _card_header("star", "Overall"),
        # Overall rating
        rx.flex(
            rx.flex(
                _field_label("How would you rate staffing, resources, and workloads overall?"),
                _check_icon(ReportState.staffing_select_overall),
                class_name="flex-row items-center justify-between",
            ),
            _emoji_rating(ReportState.staffing_select_overall, ReportState.set_staffing_select_overall),
            class_name="flex-col gap-2 px-5 py-4 border-b border-neutral-300 dark:border-neutral-800/50",
        ),
        # Comments
        _comments_field(
            ReportState.staffing_input_comments,
            ReportState.set_staffing_input_comments,
            ReportState.staffing_input_comments_chars_left,
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
                    on_click=rx.redirect(f"/report/{ReportState.mode}/assignment"),
                ),
                button(
                    "Next",
                    variant="solid",
                    on_click=[
                        ReportState.set_user_is_loading(True),
                        ReportState.handle_submit_staffing,
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
