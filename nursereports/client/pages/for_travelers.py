from ..components import button, heading, text, badge, icon
from .navbar import navbar
from .footer import footer

import reflex as rx


@rx.page(route="/for-travelers", title="Nurse Reports")
def for_travelers_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _hero(),
        _features(),
        _prose(),
        _cta_band(),
        footer(),
        class_name="flex-col items-center bg-neutral-50 dark:bg-[#07100a] w-full min-h-svh",
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

def _hero() -> rx.Component:
    return rx.flex(
        rx.box(
            class_name="wiggle-surface absolute inset-0 pointer-events-none",
        ),
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-1/2 "
                "w-[680px] h-[380px] "
                "bg-neutral-50/80 dark:bg-transparent "
                "blur-[60px] rounded-full "
                "pointer-events-none"
            ),
        ),
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-2/3 "
                "w-[800px] h-[420px] "
                "bg-emerald-500/20 dark:bg-emerald-600/15 "
                "blur-[160px] rounded-full "
                "pointer-events-none"
            ),
        ),
        rx.flex(
            badge("Travel Nurses", variant="neutral"),
            heading(
                "For Travel Nurses",
                size="2xl",
                weight="bold",
                class_name="text-center",
            ),
            text(
                "NurseReports.org creates full hospital transparency by allowing travel nurses "
                "to share detailed information on pay, culture, and experience. Compare rates "
                "between areas and know exactly what you're walking into before your next contract.",
                size="lg",
                class_name="text-center leading-relaxed max-w-screen-sm",
            ),
            button(
                "Get Started",
                on_click=rx.redirect("/create-account"),
                color="emerald",
                size="xl",
            ),
            class_name="relative flex-col items-center gap-8 w-full max-w-screen-sm z-10",
        ),
        class_name="relative flex-col items-center px-6 pt-28 pb-28 w-full overflow-hidden",
    )


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------

def _feature_card(icon_tag: str, title: str, description: str) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.box(
                class_name="wiggle-surface absolute inset-0 pointer-events-none",
            ),
            icon(icon_tag, accent=True, class_name="h-5 w-5 shrink-0 relative"),
            heading(title, size="sm", weight="semibold", class_name="ml-3 relative"),
            class_name=(
                "relative flex items-center "
                "px-5 py-4 w-full "
                "border-b border-neutral-300 dark:border-neutral-800/50"
            ),
        ),
        rx.flex(
            text(description, class_name="leading-relaxed"),
            class_name="px-5 py-5",
        ),
        class_name=(
            "flex-col w-full "
            "bg-white dark:bg-neutral-900 "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "rounded-2xl overflow-hidden"
        ),
    )


def _features() -> rx.Component:
    return rx.flex(
        rx.box(
            _feature_card(
                "bar-chart-2",
                "Rate Comparison",
                "Compare contract rates across locations, with cost-of-living context so you "
                "can evaluate assignments on equal footing.",
            ),
            _feature_card(
                "file-text",
                "Unit-Level Detail",
                "Reports down to the unit, area, and job title so there are no surprises "
                "on day one of your assignment.",
            ),
            _feature_card(
                "trending-up",
                "Rate Trends",
                "See how rates are trending over time so you can decide when to lock in — "
                "or hold out for better.",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-4 w-full max-w-screen-lg px-6",
        ),
        class_name=(
            "flex-col items-center py-20 w-full "
            "border-t border-neutral-300 dark:border-neutral-800/50 "
            "bg-neutral-100/80 dark:bg-neutral-900/50"
        ),
    )


# ---------------------------------------------------------------------------
# Prose
# ---------------------------------------------------------------------------

def _prose() -> rx.Component:
    return rx.flex(
        rx.flex(
            text(
                "In the current and future nursing shortage, travelers are a key component of the "
                "overall healthcare staffing strategy. When hospitals were overrun during the COVID "
                "pandemic, using temporary staff was the only way to maintain operational staffing "
                "levels. For many hospitals now, travelers maintain ratios and make up for call-outs "
                "and vacancies that hospitals can't fill. Many travelers use traveling as a way to "
                "visit new cities and explore areas they wouldn't otherwise have the ability to move "
                "to if they took a full-time position. Other travelers appreciate the bump in wages "
                "for the inconvenience of working a schedule that the hospital decides.",
                class_name="leading-relaxed",
            ),
            text(
                "Whatever the reason, travelers have different criteria for taking jobs than staff "
                "nurses. NurseReports.org centralizes a large repository of pay information that "
                "helps you determine not only what you get paid, but the pay context. That is to "
                "say, how do rates look like they are trending? As data is aggregated, we'll forecast "
                "the way that rates seem to be moving. We'll also offer in the future, cost-of-living "
                "adjusted rates so you can compare those rates fairly across locations.",
                class_name="leading-relaxed",
            ),
            text(
                "Travelers offer a straightforward and unique perspective into the positions they "
                "work. We want to offer you a unique set of tools to help you make the best decision "
                "for your next assignment. Details that allow you to maximize your pay, and give you "
                "details down to the unit-level to ensure you know what you are walking into. All of "
                "this starts with you taking five minutes to submit a simple report. We'll do the rest.",
                class_name="leading-relaxed",
            ),
            class_name="flex-col gap-6 w-full max-w-[680px]",
        ),
        class_name=(
            "flex-col items-center py-20 px-6 w-full "
            "border-t border-neutral-300 dark:border-neutral-800/50"
        ),
    )


# ---------------------------------------------------------------------------
# CTA band
# ---------------------------------------------------------------------------

def _cta_band() -> rx.Component:
    return rx.flex(
        rx.box(
            class_name="wiggle-surface absolute inset-0 pointer-events-none",
        ),
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-1/2 "
                "w-[340px] h-[190px] "
                "bg-neutral-50/80 dark:bg-transparent "
                "blur-[60px] rounded-full "
                "pointer-events-none"
            ),
        ),
        rx.flex(
            heading(
                "Ready to make informed decisions?",
                size="lg",
                weight="semibold",
                class_name="text-center",
            ),
            button(
                "Create Account",
                on_click=rx.redirect("/create-account"),
                color="emerald",
                size="xl",
            ),
            class_name="relative flex-col items-center gap-6 z-10",
        ),
        class_name=(
            "relative flex-col items-center justify-center "
            "border-t border-neutral-300 dark:border-neutral-800/50 "
            "bg-white/50 dark:bg-white/[0.03] "
            "backdrop-blur-md "
            "py-20 px-6 w-full overflow-hidden"
        ),
    )
