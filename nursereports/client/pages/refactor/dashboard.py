from ...components import (
    button,
    heading,
    text,
    badge,
    link,
    icon,
    report_protected,
)
from .navbar import navbar
from .footer import footer
from ....states import BaseState, HospitalState, UserState

import reflex as rx

_WIGGLE_STYLE = rx.html("""
<style>
  .wiggle-texture {
    background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='9' height='22'><path d='M4.5 0 Q7.5 5.5 4.5 11 Q1.5 16.5 4.5 22' stroke='%2310b981' stroke-width='0.75' fill='none'/></svg>");
    background-repeat: repeat;
    background-size: 9px 22px;
  }
</style>
""")


@rx.page(
    route="/dashboard",
    title="Nurse Reports",
    on_load=[
        BaseState.event_state_refresh_login,
        BaseState.event_state_requires_report,
    ],
)
@report_protected
def dashboard_page() -> rx.Component:
    return rx.flex(
        _WIGGLE_STYLE,
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-emerald-50 dark:bg-[#07100a] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        _welcome_header(),
        _stat_strip(),
        _main_grid(),
        _community_row(),
        _quick_actions(),
        class_name=(
            "flex-col gap-6 "
            "w-full max-w-screen-lg "
            "mx-auto px-4 md:px-8 py-10"
        ),
    )


# ---------------------------------------------------------------------------
# Section 1 — Welcome header
# ---------------------------------------------------------------------------

def _welcome_header() -> rx.Component:
    return rx.flex(
        # Wiggle texture overlay
        rx.box(
            class_name=(
                "wiggle-texture "
                "absolute inset-0 "
                "opacity-50 dark:opacity-10 "
                "pointer-events-none rounded-2xl"
            ),
        ),
        # Left: greeting + profile badges
        rx.flex(
            heading("Welcome back", size="lg", class_name="relative"),
            rx.flex(
                badge(UserState.user_info_license_type, variant="sky"),
                badge(UserState.user_info_license_state, variant="neutral"),
                class_name="flex-row flex-wrap gap-2 mt-2",
            ),
            class_name="flex-col relative",
        ),
        # Right: primary CTA — hidden on mobile, shown on md+
        rx.flex(
            button(
                rx.icon("file-plus", class_name="h-4 w-4"),
                "Submit a Report",
                color="emerald",
                size="md",
                on_click=rx.redirect("/report/new/overview"),
            ),
            class_name="hidden md:flex items-center relative",
        ),
        class_name=(
            "relative flex-row items-start justify-between "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl p-6 w-full overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Section 2 — Stat strip
# ---------------------------------------------------------------------------

def _stat_strip() -> rx.Component:
    return rx.flex(
        _stat_tile(UserState.user_saved_hospitals.length(), "Saved Hospitals"),
        _stat_tile(UserState.user_reports.length(), "Reports Submitted"),
        _stat_tile(UserState.user_info_license_state, "Reporting State"),
        class_name="flex-row gap-4 w-full",
    )


def _stat_tile(value, label: str) -> rx.Component:
    return rx.flex(
        rx.box(
            class_name=(
                "wiggle-texture "
                "absolute inset-0 "
                "opacity-50 dark:opacity-10 "
                "pointer-events-none rounded-2xl"
            ),
        ),
        rx.text(
            value,
            class_name=(
                "relative text-2xl font-bold tracking-tight "
                "text-neutral-950 dark:text-neutral-50"
            ),
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
# Section 3 — Main 2-col grid (Saved Hospitals + Pay Snapshot)
# ---------------------------------------------------------------------------

def _main_grid() -> rx.Component:
    return rx.flex(
        _saved_hospitals_card(),
        _pay_snapshot_card(),
        class_name="flex-col md:flex-row gap-4 w-full",
    )


# --- Saved Hospitals card ---

def _saved_hospitals_card() -> rx.Component:
    return rx.flex(
        _card_header(
            "hospital",
            "Saved Hospitals",
            button(
                rx.icon("plus", class_name="h-3.5 w-3.5"),
                "Add",
                variant="ghost",
                size="sm",
                on_click=rx.redirect("/search/hospital"),
            ),
        ),
        rx.cond(
            UserState.user_saved_hospitals,
            rx.flex(
                rx.foreach(UserState.paginated_saved_hospitals, _hospital_row),
                rx.cond(
                    UserState.num_hospital_pages > 1,
                    _hospital_pagination(),
                ),
                class_name=(
                    "flex-col divide-y "
                    "divide-neutral-100 dark:divide-neutral-800/50"
                ),
            ),
            _empty_hospitals(),
        ),
        class_name=(
            "flex-col flex-1 "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _hospital_row(hospital: dict) -> rx.Component:
    return rx.flex(
        # Hospital info
        rx.flex(
            rx.skeleton(
                text(hospital["hosp_name"], weight="medium", class_name="truncate"),
                loading=~rx.State.is_hydrated,
            ),
            rx.skeleton(
                rx.text(
                    hospital["hosp_city"],
                    ", ",
                    hospital["hosp_state"],
                    class_name="text-sm text-neutral-500 truncate",
                ),
                loading=~rx.State.is_hydrated,
            ),
            class_name="flex-col flex-1 min-w-0 justify-center",
        ),
        # Actions: trash + navigate
        rx.flex(
            _hospital_trash(hospital),
            rx.flex(
                rx.skeleton(
                    icon("arrow-right", muted=True, class_name="h-4 w-4"),
                    loading=~rx.State.is_hydrated,
                ),
                on_click=HospitalState.redirect_to_hospital_overview(hospital["hosp_id"]),
                class_name=(
                    "flex items-center justify-center "
                    "w-12 self-stretch "
                    "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                    "transition-colors duration-150 cursor-pointer"
                ),
            ),
            class_name="flex-row self-stretch",
        ),
        class_name=(
            "flex-row items-center justify-between "
            "px-5 py-3 min-h-[64px]"
        ),
    )


def _hospital_trash(hospital: dict) -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.flex(
                rx.skeleton(
                    icon("trash-2", muted=True, class_name="h-4 w-4"),
                    loading=~rx.State.is_hydrated,
                ),
                class_name=(
                    "flex items-center justify-center "
                    "w-10 self-stretch "
                    "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                    "transition-colors duration-150 cursor-pointer"
                ),
            ),
        ),
        rx.popover.content(
            rx.flex(
                text("Remove this hospital?", weight="medium"),
                rx.flex(
                    rx.popover.close(
                        button(
                            "Remove",
                            color="rose",
                            size="sm",
                            on_click=UserState.event_state_remove_hospital(
                                hospital["hosp_id"]
                            ),
                        ),
                    ),
                    rx.popover.close(
                        button("Cancel", variant="outline", size="sm"),
                    ),
                    class_name="flex-row gap-2 mt-3",
                ),
                class_name="flex-col",
            ),
        ),
    )


def _empty_hospitals() -> rx.Component:
    return rx.flex(
        icon("hospital", muted=True, class_name="h-8 w-8"),
        text("No saved hospitals yet", weight="medium", class_name="mt-3"),
        rx.text(
            "Search for hospitals to track them here.",
            class_name=(
                "text-sm text-neutral-400 dark:text-neutral-600 "
                "text-center mt-1"
            ),
        ),
        rx.flex(
            button(
                "Search Hospitals",
                variant="outline",
                size="sm",
                on_click=rx.redirect("/search/hospital"),
            ),
            class_name="mt-4",
        ),
        class_name=(
            "flex-col items-center justify-center text-center "
            "py-12 px-6"
        ),
    )


def _hospital_pagination() -> rx.Component:
    return rx.flex(
        rx.flex(
            icon("arrow-left", muted=True, class_name="h-4 w-4"),
            on_click=UserState.previous_hospital_page,
            class_name=(
                "flex items-center justify-center flex-1 py-3 "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                "transition-colors duration-150 cursor-pointer"
            ),
        ),
        rx.flex(
            rx.text(
                UserState.current_hospital_page,
                " / ",
                UserState.num_hospital_pages,
                class_name="text-sm text-neutral-400 dark:text-neutral-600",
            ),
            class_name="flex items-center justify-center flex-1 py-3",
        ),
        rx.flex(
            icon("arrow-right", muted=True, class_name="h-4 w-4"),
            on_click=UserState.next_hospital_page,
            class_name=(
                "flex items-center justify-center flex-1 py-3 "
                "hover:bg-neutral-100 dark:hover:bg-neutral-800 "
                "transition-colors duration-150 cursor-pointer"
            ),
        ),
        class_name=(
            "flex-row "
            "divide-x divide-neutral-100 dark:divide-neutral-800/50 "
            "border-t border-neutral-300 dark:border-neutral-800/50"
        ),
    )


# --- Pay Snapshot card (placeholder until DashboardState query is built) ---

def _pay_snapshot_card() -> rx.Component:
    return rx.flex(
        _card_header("banknote", "Pay Snapshot"),
        rx.flex(
            icon("chart-bar-increasing", muted=True, class_name="h-8 w-8"),
            rx.flex(
                rx.text(
                    "Pay data for ",
                    class_name="text-sm text-neutral-500",
                ),
                rx.text(
                    UserState.user_info_license_state,
                    class_name=(
                        "text-sm font-semibold "
                        "text-neutral-700 dark:text-neutral-300"
                    ),
                ),
                class_name="flex-row flex-wrap justify-center gap-1 mt-3",
            ),
            rx.text(
                "State and national pay averages are coming soon.",
                class_name=(
                    "text-sm text-neutral-400 dark:text-neutral-600 "
                    "text-center mt-1"
                ),
            ),
            rx.flex(
                link(
                    "Explore hospitals in your state →",
                    href="/search/hospital",
                    accent=True,
                    class_name="text-sm",
                ),
                class_name="mt-4",
            ),
            class_name=(
                "flex-col flex-1 items-center justify-center text-center "
                "py-12 px-6"
            ),
        ),
        class_name=(
            "flex-col flex-1 "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Section 4 — Community row (Trending + Your Contribution)
# ---------------------------------------------------------------------------

def _community_row() -> rx.Component:
    return rx.flex(
        _trending_card(),
        _contribution_card(),
        class_name="flex-col md:flex-row gap-4 w-full",
    )


def _trending_card() -> rx.Component:
    return rx.flex(
        _card_header("trending-up", "Trending in Your State"),
        rx.flex(
            icon("clock", muted=True, class_name="h-7 w-7"),
            text("Coming soon", weight="medium", class_name="mt-3"),
            rx.text(
                "Recently reviewed hospitals in your state will appear here.",
                class_name=(
                    "text-sm text-neutral-400 dark:text-neutral-600 "
                    "text-center mt-1"
                ),
            ),
            class_name=(
                "flex-col flex-1 items-center justify-center text-center "
                "py-10 px-6"
            ),
        ),
        class_name=(
            "flex-col flex-1 "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _contribution_card() -> rx.Component:
    return rx.flex(
        _card_header("heart", "Your Contribution"),
        rx.cond(
            UserState.user_reports,
            # Has reports
            rx.flex(
                rx.text(
                    UserState.user_reports.length(),
                    class_name=(
                        "text-4xl font-bold tracking-tight "
                        "text-emerald-600 dark:text-emerald-500"
                    ),
                ),
                rx.text(
                    rx.cond(
                        UserState.user_reports.length() == 1,
                        "report submitted",
                        "reports submitted",
                    ),
                    class_name="text-sm text-neutral-500 mt-1",
                ),
                rx.text(
                    "Your reports help nurses across the country "
                    "make informed career decisions.",
                    class_name=(
                        "text-sm text-neutral-400 dark:text-neutral-600 "
                        "text-center mt-3 max-w-[240px]"
                    ),
                ),
                class_name=(
                    "flex-col flex-1 items-center justify-center text-center "
                    "py-10 px-6"
                ),
            ),
            # No reports yet
            rx.flex(
                icon("file-text", muted=True, class_name="h-7 w-7"),
                text("No reports yet", weight="medium", class_name="mt-3"),
                rx.text(
                    "Submit your first report to start contributing "
                    "to the community.",
                    class_name=(
                        "text-sm text-neutral-400 dark:text-neutral-600 "
                        "text-center mt-1"
                    ),
                ),
                rx.flex(
                    button(
                        "Submit a Report",
                        color="emerald",
                        size="sm",
                        on_click=rx.redirect("/report/new/overview"),
                    ),
                    class_name="mt-4",
                ),
                class_name=(
                    "flex-col flex-1 items-center justify-center text-center "
                    "py-10 px-6"
                ),
            ),
        ),
        class_name=(
            "flex-col flex-1 "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


# ---------------------------------------------------------------------------
# Section 5 — Quick Actions
# ---------------------------------------------------------------------------

def _quick_actions() -> rx.Component:
    return rx.flex(
        _action_card(
            "search",
            "Search Hospitals",
            "Find and compare hospitals by state and city.",
            "/search/hospital",
        ),
        _action_card(
            "file-plus",
            "Submit a Report",
            "Share your experience to help the community.",
            "/report/new/overview",
        ),
        _action_card(
            "circle-user-round",
            "My Account",
            "View your profile, reports, and account settings.",
            "/my-account",
        ),
        class_name="flex-col md:flex-row gap-4 w-full",
    )


def _action_card(
    icon_tag: str, title: str, description: str, href: str
) -> rx.Component:
    return rx.flex(
        icon(icon_tag, accent=True, class_name="h-6 w-6"),
        text(title, weight="semibold", class_name="mt-3"),
        rx.text(
            description,
            class_name=(
                "text-sm text-neutral-400 dark:text-neutral-600 "
                "text-center mt-1 flex-1"
            ),
        ),
        rx.flex(
            link("Go →", href=href, accent=True, class_name="text-sm font-medium"),
            class_name="mt-4",
        ),
        class_name=(
            "flex-col flex-1 items-center text-center "
            "bg-emerald-500/20 dark:bg-white/[0.03] "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl p-6 "
            "hover:border-emerald-300 dark:hover:border-emerald-800 "
            "transition-colors duration-150"
        ),
    )


# ---------------------------------------------------------------------------
# Shared card header helper
# ---------------------------------------------------------------------------

def _card_header(icon_tag: str, title: str, action=None) -> rx.Component:
    return rx.flex(
        rx.box(
            class_name=(
                "wiggle-texture "
                "absolute inset-0 "
                "opacity-50 dark:opacity-10 "
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
            "px-5 py-4 overflow-hidden "
            "border-b border-neutral-300 dark:border-neutral-800/50"
        ),
    )
