from ..components import (
    badge,
    button,
    heading,
    text,
    icon,
    report_protected,
)
from .navbar import navbar
from .footer import footer
from ...states import BaseState, HospitalState, ReportState, UserState

import reflex as rx


@rx.page(
    route="/hospital/[cms_id]",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_report,
        HospitalState.event_state_load_hospital_info,
    ],
)
@report_protected
def hospital_overview_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        _hospital_header(),
        _pay_section(),
        _ratings_section(),
        _reviews_section(),
        class_name=(
            "flex-col gap-4 md:gap-8 "
            "w-full max-w-screen-lg "
            "px-4 md:px-8 pt-4 md:pt-16 pb-24 md:pb-48"
        ),
    )


# ---------------------------------------------------------------------------
# Section 1 — Hospital header
# ---------------------------------------------------------------------------

def _hospital_header() -> rx.Component:
    return rx.flex(
        # Wiggle texture overlay
        rx.box(
            class_name=(
                "wiggle-card absolute inset-0 "
                "pointer-events-none rounded-2xl"
            ),
        ),
        # Top row: name/address + desktop buttons
        rx.flex(
            # Left: name + address + badges
            rx.flex(
                rx.skeleton(
                    heading(
                        HospitalState.hospital_info["hosp_name"],
                        size="lg",
                        class_name="relative",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                rx.skeleton(
                    text(
                        HospitalState.hospital_info["hosp_addr"],
                        class_name="relative text-neutral-500 dark:text-neutral-400 mt-0.5",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                rx.skeleton(
                    text(
                        HospitalState.hospital_info["hosp_city"],
                        ", ",
                        HospitalState.hospital_info["hosp_state_abbr"],
                        " ",
                        HospitalState.hospital_info["hosp_zip"],
                        class_name="relative text-neutral-500 dark:text-neutral-400",
                    ),
                    loading=~rx.State.is_hydrated,
                ),
                class_name="flex-col relative",
            ),
            # Right: action buttons — desktop only
            rx.flex(
                button(
                    "Submit Report",
                    color="emerald",
                    size="md",
                    on_click=ReportState.event_state_create_full_report(HospitalState.hosp_id),
                ),
                button(
                    icon("bookmark-plus", class_name="h-4 w-4"),
                    "Save Hospital",
                    variant="outline",
                    size="md",
                    on_click=UserState.event_state_add_hospital(HospitalState.hosp_id),
                ),
                class_name="flex-col gap-2 relative hidden md:flex shrink-0",
            ),
            class_name="flex-row items-start justify-between relative w-full",
        ),
        # Mobile-only buttons row
        rx.flex(
            rx.flex(
                button(
                    icon("bookmark-plus", class_name="h-4 w-4"),
                    "Save Hospital",
                    variant="outline",
                    size="md",
                    width="full",
                    on_click=UserState.event_state_add_hospital(HospitalState.hosp_id),
                ),
                class_name="flex-1",
            ),
            rx.flex(
                button(
                    "Submit Report",
                    color="emerald",
                    size="md",
                    width="full",
                    on_click=ReportState.event_state_create_full_report(HospitalState.hosp_id),
                ),
                class_name="flex-1",
            ),
            class_name="flex md:hidden flex-row gap-2 pt-4 relative w-full",
        ),
        class_name=(
            "relative flex-col "
            "bg-emerald-500/30 dark:bg-white/[0.06] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl p-6 w-full overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Section 2 — Stat strip
# ---------------------------------------------------------------------------

def _stat_strip() -> rx.Component:
    return rx.flex(
        _stat_tile(
            HospitalState.report_info.length(),
            "Reports",
            sky=False,
        ),
        rx.cond(
            HospitalState.overall_hospital_scores,
            _stat_tile(
                HospitalState.overall_hospital_scores["overall"],
                "Overall Score",
                sky=True,
            ),
            _stat_tile("—", "Overall Score", sky=True),
        ),
        rx.cond(
            HospitalState.extrapolated_ft_pay_hospital,
            _stat_tile(
                HospitalState.ft_pay_hospital_formatted["hourly"],
                "Est. FT Hourly",
                sky=True,
            ),
            _stat_tile("—", "Est. FT Hourly", sky=True),
        ),
        class_name="flex-row gap-4 w-full",
    )


def _stat_tile(value, label: str, sky: bool = False) -> rx.Component:
    value_class = (
        "relative text-2xl font-bold font-mono tracking-tight "
        + ("text-sky-600 dark:text-sky-400" if sky else "text-neutral-950 dark:text-neutral-50")
    )
    return rx.flex(
        rx.box(
            class_name=(
                "wiggle-card absolute inset-0 "
                "pointer-events-none rounded-2xl"
            ),
        ),
        rx.skeleton(
            rx.text(value, class_name=value_class),
            loading=~rx.State.is_hydrated,
        ),
        rx.text(
            label,
            class_name="relative text-sm text-neutral-500 dark:text-neutral-500 mt-0.5",
        ),
        class_name=(
            "relative flex-col flex-1 items-center justify-center text-center "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl p-5 overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Section 3 — Pay
# ---------------------------------------------------------------------------

def _pay_section() -> rx.Component:
    return rx.flex(
        _pay_card_header(),
        rx.cond(
            HospitalState.extrapolated_ft_pay_hospital
            | HospitalState.extrapolated_pt_pay_hospital
            | HospitalState.averaged_contract_pay_hospital
            | HospitalState.extrapolated_ft_pay_state
            | HospitalState.extrapolated_pt_pay_state
            | HospitalState.averaged_contract_pay_state,
            rx.fragment(
                _pay_experience_context(),
                _pay_values(),
                _pay_callouts(),
            ),
            rx.flex(
                icon("banknote", muted=True, class_name="h-8 w-8"),
                text("No pay info yet", weight="medium", class_name="mt-3"),
                rx.text(
                    "Pay data will appear once nurses submit reports for this hospital.",
                    class_name=(
                        "text-sm text-neutral-400 dark:text-neutral-600 "
                        "text-center mt-1 max-w-xs"
                    ),
                ),
                class_name=(
                    "flex-col items-center justify-center text-center "
                    "py-12 px-6"
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


def _pay_card_header() -> rx.Component:
    return _card_header("banknote", "Staff Pay")


def _pay_experience_context() -> rx.Component:
    """Context row: employment type selector + advanced pay curve link."""
    return rx.flex(
        rx.flex(
            rx.select(
                ["Full-time", "Part-time", "Contract"],
                value=HospitalState.selected_hospital_average,
                on_change=HospitalState.setvar("selected_hospital_average"),
                size="1",
            ),
            rx.cond(
                HospitalState.selected_hospital_average != "Contract",
                _pay_graph(),
            ),
            class_name=(
                "flex-row items-center justify-between "
                "px-5 py-2.5 "
                "border-b border-neutral-300 dark:border-neutral-800/50"
            ),
        ),
        class_name="flex-col",
    )


def _pay_graph() -> rx.Component:
    """Dialog with recharts line chart showing full pay curve."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.flex(
                icon("chart-line", muted=True, class_name="h-3.5 w-3.5"),
                rx.text(
                    "Pay Curve",
                    class_name="text-xs text-neutral-400 dark:text-neutral-600",
                ),
                class_name=(
                    "flex-row items-center gap-1.5 cursor-pointer "
                    "hover:text-neutral-700 dark:hover:text-neutral-300 "
                    "transition-colors duration-150"
                ),
            ),
        ),
        rx.dialog.content(
            rx.flex(
                # Dialog header
                rx.flex(
                    rx.flex(
                        icon("chart-line", accent=True, class_name="h-5 w-5"),
                        heading("Pay Curve", size="sm"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.dialog.close(
                        icon("x", muted=True, class_name="h-5 w-5 cursor-pointer"),
                    ),
                    class_name="flex-row items-center justify-between w-full pb-4",
                ),
                # Subtitle
                text(
                    HospitalState.hospital_info["hosp_name"],
                    " vs ",
                    HospitalState.hospital_info["hosp_state"],
                    " average — ",
                    HospitalState.selected_hospital_average,
                    size="sm",
                    class_name="text-neutral-500 pb-4",
                ),
                # Chart
                rx.cond(
                    HospitalState.pay_chart_data,
                    rx.recharts.line_chart(
                        rx.recharts.line(
                            data_key="Hospital",
                            stroke="#10b981",
                            stroke_width=2,
                            dot=False,
                        ),
                        rx.recharts.line(
                            data_key="State",
                            stroke="#0ea5e9",
                            stroke_width=2,
                            dot=False,
                            stroke_dasharray="4 4",
                        ),
                        rx.recharts.x_axis(
                            data_key="year",
                            label={"value": "Years Experience", "position": "insideBottom", "offset": -4},
                        ),
                        rx.recharts.y_axis(
                            tick_formatter="(v) => `$${v}`",
                        ),
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3", opacity=0.3),
                        rx.recharts.graphing_tooltip(
                            formatter="(v) => [`$${v}/hr`]",
                        ),
                        rx.recharts.legend(),
                        data=HospitalState.pay_chart_data,
                        width="100%",
                        height=280,
                        margin={"top": 8, "right": 8, "bottom": 24, "left": 8},
                    ),
                    rx.flex(
                        icon("ban", muted=True, class_name="h-6 w-6"),
                        text("No pay data available for chart.", class_name="mt-2 text-neutral-400"),
                        class_name="flex-col items-center justify-center py-16",
                    ),
                ),
                # Legend note
                rx.flex(
                    rx.flex(
                        rx.box(class_name="w-4 h-0.5 bg-emerald-500 rounded shrink-0"),
                        text("Hospital", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.flex(
                        rx.box(class_name="w-4 h-px border-t-2 border-dashed border-sky-500 shrink-0"),
                        text("State average", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    class_name="flex-row gap-6 pt-2",
                ),
                class_name="flex-col w-full",
            ),
            class_name="max-w-2xl w-full",
        ),
    )


def _pay_values() -> rx.Component:
    return rx.flex(
        # Hospital average
        rx.flex(
            text("Hospital Average", size="sm", class_name="text-neutral-500 mb-3"),
            rx.cond(
                HospitalState.selected_hospital_average != "Contract",
                # FT / PT — show hourly + yearly
                rx.flex(
                    rx.cond(
                        HospitalState.selected_hospital_average == "Full-time",
                        rx.cond(
                            HospitalState.extrapolated_ft_pay_hospital,
                            _pay_stat_pair(
                                HospitalState.ft_pay_hospital_formatted["hourly"],
                                HospitalState.ft_pay_hospital_formatted["yearly"],
                            ),
                            _no_pay_state(),
                        ),
                        rx.cond(
                            HospitalState.extrapolated_pt_pay_hospital,
                            _pay_stat_pair(
                                HospitalState.pt_pay_hospital_formatted["hourly"],
                                HospitalState.pt_pay_hospital_formatted["yearly"],
                            ),
                            _no_pay_state(),
                        ),
                    ),
                    class_name="flex-row gap-6",
                ),
                # Contract — show weekly
                rx.cond(
                    HospitalState.averaged_contract_pay_hospital,
                    rx.flex(
                        rx.skeleton(
                            rx.text(
                                HospitalState.averaged_contract_pay_hospital.get("averaged_weekly", "—"),
                                class_name=(
                                    "text-2xl font-bold font-mono "
                                    "text-sky-600 dark:text-sky-400"
                                ),
                            ),
                            loading=~rx.State.is_hydrated,
                        ),
                        text("/ WEEK (AVG)", size="xs", class_name="text-neutral-400 mt-1 uppercase tracking-wide"),
                        class_name="flex-col items-start",
                    ),
                    _no_pay_state(),
                ),
            ),
            class_name="flex-col flex-1 px-5 py-4",
        ),
        # Divider
        rx.box(class_name="w-px bg-neutral-300 dark:bg-neutral-800/50 self-stretch"),
        # State average
        rx.flex(
            text(
                HospitalState.hospital_info["hosp_state"],
                " Average",
                size="sm",
                class_name="text-neutral-500 mb-3",
            ),
            rx.cond(
                HospitalState.selected_hospital_average != "Contract",
                rx.flex(
                    rx.cond(
                        HospitalState.selected_hospital_average == "Full-time",
                        rx.cond(
                            HospitalState.extrapolated_ft_pay_state,
                            _pay_stat_pair(
                                HospitalState.ft_pay_state_formatted["hourly"],
                                HospitalState.ft_pay_state_formatted["yearly"],
                            ),
                            _no_pay_state(),
                        ),
                        rx.cond(
                            HospitalState.extrapolated_pt_pay_state,
                            _pay_stat_pair(
                                HospitalState.pt_pay_state_formatted["hourly"],
                                HospitalState.pt_pay_state_formatted["yearly"],
                            ),
                            _no_pay_state(),
                        ),
                    ),
                    class_name="flex-row gap-6",
                ),
                rx.cond(
                    HospitalState.averaged_contract_pay_state,
                    rx.flex(
                        rx.skeleton(
                            rx.text(
                                HospitalState.averaged_contract_pay_state.get("averaged_weekly", "—"),
                                class_name=(
                                    "text-2xl font-bold font-mono "
                                    "text-sky-600 dark:text-sky-400"
                                ),
                            ),
                            loading=~rx.State.is_hydrated,
                        ),
                        text("/ WEEK (AVG)", size="xs", class_name="text-neutral-400 mt-1 uppercase tracking-wide"),
                        class_name="flex-col items-start",
                    ),
                    _no_pay_state(),
                ),
            ),
            class_name="flex-col flex-1 px-5 py-4",
        ),
        class_name=(
            "flex-row "
            "border-b border-neutral-300 dark:border-neutral-800/50"
        ),
    )


def _pay_stat_pair(hourly, yearly) -> rx.Component:
    return rx.flex(
        # Hourly: mobile = "$42.00 / hr" inline; desktop = "$42.00" then "/ HR" below
        rx.flex(
            rx.skeleton(
                rx.text(
                    hourly,
                    class_name=(
                        "text-2xl font-bold font-mono "
                        "text-sky-600 dark:text-sky-400"
                    ),
                ),
                loading=~rx.State.is_hydrated,
            ),
            text(
                "/ HR",
                size="xs",
                class_name=(
                    "text-neutral-400 uppercase tracking-wide "
                    "ml-1.5 mb-0.5 md:ml-0 md:mb-0 md:mt-1"
                ),
            ),
            class_name="flex-row md:flex-col items-end md:items-start gap-0",
        ),
        # Yearly: mobile = "$78,000 / yr" inline; desktop = "$78,000" then "/ YR" below
        rx.flex(
            rx.skeleton(
                rx.text(
                    yearly,
                    class_name=(
                        "text-2xl font-bold font-mono "
                        "text-sky-600 dark:text-sky-400"
                    ),
                ),
                loading=~rx.State.is_hydrated,
            ),
            text(
                "/ YR",
                size="xs",
                class_name=(
                    "text-neutral-400 uppercase tracking-wide "
                    "ml-1.5 mb-0.5 md:ml-0 md:mb-0 md:mt-1"
                ),
            ),
            class_name="flex-row md:flex-col items-end md:items-start gap-0",
        ),
        class_name="flex-col md:flex-row gap-1 md:gap-6",
    )


def _no_pay_state() -> rx.Component:
    return rx.flex(
        icon("ban", muted=True, class_name="h-5 w-5"),
        text("No data yet", class_name="text-sm text-neutral-400 dark:text-neutral-600 ml-2"),
        class_name="flex-row items-center py-2",
    )


def _pay_callouts() -> rx.Component:
    return rx.flex(
        # Experience context
        rx.cond(
            HospitalState.selected_hospital_average != "Contract",
            rx.flex(
                rx.cond(
                    UserState.user_info_experience > 0,
                    text(
                        "Based on your ",
                        rx.text.span(
                            UserState.user_info_experience,
                            " year",
                            rx.cond(UserState.user_info_experience == 1, "", "s"),
                            " of experience.",
                            class_name="font-medium text-neutral-700 dark:text-neutral-300",
                        ),
                        size="sm",
                        class_name="text-neutral-400 dark:text-neutral-600",
                    ),
                    text(
                        "Based on your experience (update in My Account)",
                        size="sm",
                        class_name="text-neutral-400 dark:text-neutral-600",
                    ),
                ),
                class_name="px-5 py-3 border-b border-neutral-300 dark:border-neutral-800/50",
            ),
        ),
        # FT limited
        rx.cond(
            (HospitalState.selected_hospital_average == "Full-time") &
            HospitalState.ft_pay_hospital_info_limited &
            HospitalState.extrapolated_ft_pay_hospital,
            rx.flex(
                icon("triangle-alert", class_name="h-4 w-4 text-amber-600 dark:text-amber-400 shrink-0"),
                text(
                    "Limited data. Estimates may be more inaccurate.",
                    size="sm",
                    class_name="text-amber-700 dark:text-amber-400",
                ),
                class_name="flex-row items-center gap-2 px-5 py-3",
            ),
        ),
        # PT limited
        rx.cond(
            (HospitalState.selected_hospital_average == "Part-time") &
            HospitalState.pt_pay_hospital_info_limited &
            HospitalState.extrapolated_pt_pay_hospital,
            rx.flex(
                icon("triangle-alert", class_name="h-4 w-4 text-amber-600 dark:text-amber-400 shrink-0"),
                text(
                    "Limited data. Estimates may be more inaccurate.",
                    size="sm",
                    class_name="text-amber-700 dark:text-amber-400",
                ),
                class_name="flex-row items-center gap-2 px-5 py-3",
            ),
        ),
        # Contract limited
        rx.cond(
            (HospitalState.selected_hospital_average == "Contract") &
            HospitalState.contract_pay_info_hospital_limited &
            HospitalState.averaged_contract_pay_hospital,
            rx.flex(
                icon("triangle-alert", class_name="h-4 w-4 text-amber-600 dark:text-amber-400 shrink-0"),
                text(
                    "Limited data. Average may be more inaccurate.",
                    size="sm",
                    class_name="text-amber-700 dark:text-amber-400",
                ),
                class_name="flex-row items-center gap-2 px-5 py-3",
            ),
        ),
        class_name="flex-col",
    )


# ---------------------------------------------------------------------------
# Section 4 — Ratings
# ---------------------------------------------------------------------------

def _ranking_dialog() -> rx.Component:
    """Dialog with a sortable table ranking all units by score."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.flex(
                icon("list-ordered", muted=True, class_name="h-3.5 w-3.5"),
                rx.text(
                    "Unit Rankings",
                    class_name="text-xs text-neutral-400 dark:text-neutral-600",
                ),
                class_name=(
                    "flex-row items-center gap-1.5 cursor-pointer "
                    "hover:text-neutral-700 dark:hover:text-neutral-300 "
                    "transition-colors duration-150"
                ),
            ),
        ),
        rx.dialog.content(
            rx.flex(
                # Card header
                rx.flex(
                    rx.flex(
                        icon("list-ordered", accent=True, class_name="h-5 w-5"),
                        heading("Unit Rankings", size="sm"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.flex(
                        text(
                            "Click a column header to sort.",
                            size="xs",
                            class_name="text-neutral-400 dark:text-neutral-600 italic",
                        ),
                        rx.dialog.close(
                            icon("x", muted=True, class_name="h-5 w-5 cursor-pointer"),
                        ),
                        class_name="flex-row items-center gap-4",
                    ),
                    class_name=(
                        "flex-row items-center justify-between w-full "
                        "px-5 py-4 bg-emerald-500/10 dark:bg-white/[0.03] "
                        "border-b border-neutral-300 dark:border-neutral-800/50"
                    ),
                ),
                # Table header row
                rx.flex(
                    rx.flex(
                        text("Unit", size="xs", class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-wide"),
                        class_name="flex-1 min-w-0",
                    ),
                    _ratings_sort_header("Comp", "comp_overall"),
                    _ratings_sort_header("Assign", "assign_overall"),
                    _ratings_sort_header("Staff", "staff_overall"),
                    _ratings_sort_header("Overall", "overall"),
                    class_name=(
                        "flex-row items-center gap-2 px-4 py-2.5 "
                        "border-b border-neutral-300 dark:border-neutral-800/50"
                    ),
                ),
                # Scrollable rows
                rx.flex(
                    rx.foreach(HospitalState.sorted_ratings_table, _ratings_table_row),
                    class_name="flex-col overflow-y-auto max-h-80",
                ),
                # Score scale
                rx.flex(
                    rx.flex(
                        rx.box(class_name="w-4 h-4 rounded bg-rose-300 dark:bg-rose-700 shrink-0"),
                        text("Terrible", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.flex(
                        rx.box(class_name="w-4 h-4 rounded bg-amber-300 dark:bg-orange-700 shrink-0"),
                        text("Bad", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.flex(
                        rx.box(class_name="w-4 h-4 rounded bg-yellow-200 dark:bg-yellow-500 shrink-0"),
                        text("OK", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.flex(
                        rx.box(class_name="w-4 h-4 rounded bg-emerald-300 dark:bg-emerald-700 shrink-0"),
                        text("Good", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    rx.flex(
                        rx.box(class_name="w-4 h-4 rounded bg-sky-300 dark:bg-sky-700 shrink-0"),
                        text("Great", size="xs", class_name="text-neutral-500"),
                        class_name="flex-row items-center gap-2",
                    ),
                    class_name=(
                        "flex-row flex-wrap gap-x-5 gap-y-2 "
                        "px-5 py-3 "
                        "border-t border-neutral-300 dark:border-neutral-800/50"
                    ),
                ),
                class_name=(
                    "flex-col w-full "
                    "bg-emerald-500/20 dark:bg-white/[0.03] "
                    "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
                    "rounded-2xl overflow-hidden"
                ),
            ),
            class_name="max-w-2xl w-full !bg-white dark:!bg-[#0f1f13] shadow-none p-0",
        ),
    )


def _ratings_sort_header(label: str, col_key: str) -> rx.Component:
    return rx.flex(
        text(
            label,
            size="xs",
            class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-wide",
        ),
        rx.cond(
            HospitalState.ratings_sort_col == col_key,
            rx.cond(
                HospitalState.ratings_sort_asc,
                icon("chevron-up", muted=True, class_name="h-3 w-3"),
                icon("chevron-down", muted=True, class_name="h-3 w-3"),
            ),
            rx.fragment(),
        ),
        on_click=HospitalState.set_ratings_sort(col_key),
        class_name="w-20 flex-row items-center justify-center gap-1 cursor-pointer select-none hover:text-neutral-700 dark:hover:text-neutral-300 transition-colors duration-150",
    )


def _ratings_table_row(row: dict) -> rx.Component:
    return rx.flex(
        rx.flex(
            text(row["units_areas_roles"], size="sm", class_name="truncate"),
            class_name="flex-1 min-w-0",
        ),
        _ratings_float_cell(row["comp_display"], row["comp_tier"]),
        _ratings_float_cell(row["assign_display"], row["assign_tier"]),
        _ratings_float_cell(row["staff_display"], row["staff_tier"]),
        _ratings_float_cell(row["overall_display"], row["overall_tier"]),
        class_name=(
            "flex-row items-center gap-2 px-4 py-2.5 min-h-11 overflow-hidden shrink-0 "
            "border-b border-neutral-200 dark:border-neutral-800/50 "
            "last:border-b-0"
        ),
    )


def _ratings_float_cell(display, tier) -> rx.Component:
    text_class = "text-sm font-mono font-medium text-neutral-800 dark:text-neutral-100"
    return rx.flex(
        rx.text(display, class_name=text_class),
        class_name=rx.match(
            tier,
            (5, "w-20 items-center justify-center rounded-md bg-sky-300 dark:bg-sky-700 py-1"),
            (4, "w-20 items-center justify-center rounded-md bg-emerald-300 dark:bg-emerald-700 py-1"),
            (3, "w-20 items-center justify-center rounded-md bg-yellow-200 dark:bg-yellow-500 py-1"),
            (2, "w-20 items-center justify-center rounded-md bg-amber-300 dark:bg-orange-700 py-1"),
            "w-20 items-center justify-center rounded-md bg-rose-300 dark:bg-rose-700 py-1",
        ),
    )


def _ratings_section() -> rx.Component:
    return rx.flex(
        _card_header("star", "Ratings"),
        # Context row: unit selector + advanced rankings
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            rx.flex(
                rx.select(
                    HospitalState.units_areas_roles_for_units,
                    value=HospitalState.selected_unit,
                    on_change=HospitalState.set_selected_unit,
                    size="1",
                ),
                _ranking_dialog(),
                class_name=(
                    "flex-row items-center justify-between "
                    "px-5 py-2.5 "
                    "border-b border-neutral-300 dark:border-neutral-800/50"
                ),
            ),
        ),
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            rx.flex(
                _rating_tile(
                    "Compensation",
                    HospitalState.selected_unit_display["comp_overall_display"],
                    HospitalState.selected_unit_display["comp_overall_tier"],
                    "How satisfied nurses are with overall pay and benefits.",
                ),
                _rating_tile(
                    "Assignment",
                    HospitalState.selected_unit_display["assign_overall_display"],
                    HospitalState.selected_unit_display["assign_overall_tier"],
                    "Workplace culture, teamwork, management, and day-to-day experience.",
                ),
                _rating_tile(
                    "Staffing",
                    HospitalState.selected_unit_display["staff_overall_display"],
                    HospitalState.selected_unit_display["staff_overall_tier"],
                    "How fair nurse-to-patient ratios and daily workloads feel.",
                ),
                class_name=(
                    "flex-col md:flex-row w-full "
                    "divide-y md:divide-y-0 md:divide-x "
                    "divide-neutral-300 dark:divide-neutral-800/50"
                ),
            ),
            rx.flex(
                icon("star", muted=True, class_name="h-8 w-8"),
                text("No reports yet", weight="medium", class_name="mt-3"),
                rx.text(
                    "Ratings will appear once nurses submit reports for this hospital.",
                    class_name=(
                        "text-sm text-neutral-400 dark:text-neutral-600 "
                        "text-center mt-1 max-w-xs"
                    ),
                ),
                class_name=(
                    "flex-col items-center justify-center text-center "
                    "py-12 px-6"
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


def _rating_tile(label: str, display, tier, description: str) -> rx.Component:
    return rx.flex(
        text(
            label.upper(),
            size="xs",
            class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-widest text-left md:text-center",
        ),
        # Score group: horizontal on mobile (number + /5 inline), vertical on md+
        rx.flex(
            rx.skeleton(
                rx.match(
                    tier,
                    (5, rx.text(display, class_name="text-2xl md:text-4xl font-bold font-mono tracking-tight text-sky-600 dark:text-sky-400")),
                    (4, rx.text(display, class_name="text-2xl md:text-4xl font-bold font-mono tracking-tight text-emerald-600 dark:text-emerald-500")),
                    (3, rx.text(display, class_name="text-2xl md:text-4xl font-bold font-mono tracking-tight text-yellow-500 dark:text-yellow-400")),
                    (2, rx.text(display, class_name="text-2xl md:text-4xl font-bold font-mono tracking-tight text-amber-600 dark:text-amber-400")),
                    (1, rx.text(display, class_name="text-2xl md:text-4xl font-bold font-mono tracking-tight text-rose-600 dark:text-rose-400")),
                    rx.text(display, class_name="text-2xl md:text-4xl font-bold font-mono tracking-tight text-neutral-400 dark:text-neutral-600"),
                ),
                loading=~rx.State.is_hydrated,
            ),
            rx.flex(
                text("/ 5", size="xs", class_name="text-neutral-400 dark:text-neutral-600"),
                rx.tooltip(
                    icon("circle-help", muted=True, class_name="h-3.5 w-3.5 cursor-help"),
                    content=description,
                    delay_duration=200,
                ),
                class_name="flex-row items-center gap-2",
            ),
            class_name="flex-row items-center gap-2 md:flex-col md:items-center md:gap-1",
        ),
        class_name=(
            "flex-row items-center justify-between "
            "md:flex-col md:items-center md:justify-center md:text-center "
            "flex-1 px-4 py-3 md:py-6 gap-2 md:gap-1"
        ),
    )


# ---------------------------------------------------------------------------
# Section 5 — Reviews
# ---------------------------------------------------------------------------

def _reviews_section() -> rx.Component:
    return rx.flex(
        _card_header("message-circle", "Reviews"),
        # Context row: unit selector
        rx.cond(
            HospitalState.units_areas_roles_for_units,
            rx.flex(
                rx.select(
                    HospitalState.units_areas_roles_for_units,
                    value=HospitalState.selected_review_unit,
                    on_change=HospitalState.set_selected_review_unit,
                    size="1",
                ),
                class_name=(
                    "flex-row items-center "
                    "px-5 py-2.5 "
                    "border-b border-neutral-300 dark:border-neutral-800/50"
                ),
            ),
        ),
        rx.cond(
            HospitalState.review_info,
            rx.flex(
                rx.flex(
                    rx.foreach(HospitalState.paginated_review_info, _review_card),
                    class_name=(
                        "flex-col divide-y "
                        "divide-neutral-300 dark:divide-neutral-800/50"
                    ),
                ),
                rx.box(class_name="flex-1"),
                rx.cond(
                    HospitalState.num_review_pages > 1,
                    _review_pagination(),
                ),
                class_name="flex-col flex-1",
            ),
            rx.flex(
                icon("message-circle", muted=True, class_name="h-8 w-8"),
                text("No reviews yet", weight="medium", class_name="mt-3"),
                rx.text(
                    "Reviews will appear once nurses submit reports with comments.",
                    class_name=(
                        "text-sm text-neutral-400 dark:text-neutral-600 "
                        "text-center mt-1 max-w-xs"
                    ),
                ),
                class_name=(
                    "flex-col items-center justify-center text-center "
                    "py-12 px-6"
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


def _review_card(review: dict) -> rx.Component:
    return rx.flex(
        # Header row: unit badge + timestamp
        rx.flex(
            rx.skeleton(
                badge(review["units_areas_roles"], variant="sky"),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                text(
                    review["time_ago"],
                    size="xs",
                    class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-wide whitespace-nowrap",
                ),
                loading=~rx.State.is_hydrated,
            ),
            class_name="flex-row items-center justify-between gap-3 w-full",
        ),
        # Comment rows
        rx.cond(
            review["comp_comments"],
            rx.flex(
                text(
                    "Compensation",
                    size="xs",
                    class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-widest shrink-0 mt-0.5",
                ),
                text(review["comp_comments"], size="sm"),
                class_name="flex-col gap-1 w-full",
            ),
        ),
        rx.cond(
            review["assign_comments"],
            rx.flex(
                text(
                    "Assignment",
                    size="xs",
                    class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-widest shrink-0 mt-0.5",
                ),
                text(review["assign_comments"], size="sm"),
                class_name="flex-col gap-1 w-full",
            ),
        ),
        rx.cond(
            review["staff_comments"],
            rx.flex(
                text(
                    "Staffing",
                    size="xs",
                    class_name="text-neutral-400 dark:text-neutral-600 uppercase tracking-widest shrink-0 mt-0.5",
                ),
                text(review["staff_comments"], size="sm"),
                class_name="flex-col gap-1 w-full",
            ),
        ),
        class_name="flex-col gap-3 px-5 py-4 w-full",
    )


def _review_pagination() -> rx.Component:
    return rx.flex(
        rx.flex(
            icon("arrow-left", muted=True, class_name="h-4 w-4"),
            on_click=HospitalState.previous_review_page,
            class_name=(
                "flex items-center justify-center flex-1 py-3 "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                "transition-colors duration-150 cursor-pointer"
            ),
        ),
        rx.flex(
            rx.text(
                HospitalState.current_review_page,
                " / ",
                HospitalState.num_review_pages,
                class_name="text-sm text-neutral-400 dark:text-neutral-600",
            ),
            class_name="flex items-center justify-center flex-1 py-3",
        ),
        rx.flex(
            icon("arrow-right", muted=True, class_name="h-4 w-4"),
            on_click=HospitalState.next_review_page,
            class_name=(
                "flex items-center justify-center flex-1 py-3 "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                "transition-colors duration-150 cursor-pointer"
            ),
        ),
        class_name=(
            "flex-row "
            "divide-x divide-neutral-300 dark:divide-neutral-800/50 "
            "border-t border-neutral-300 dark:border-neutral-800/50"
        ),
    )


# ---------------------------------------------------------------------------
# Shared card header helper (mirrors dashboard._card_header)
# ---------------------------------------------------------------------------

def _card_header(icon_tag: str, title: str, action=None) -> rx.Component:
    return rx.flex(
        rx.box(
            class_name=(
                "absolute inset-0 "
                "pointer-events-none"
            ),
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
