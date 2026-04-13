from ...components import button, heading, text, badge, icon
from .navbar import navbar
from .footer import footer

import reflex as rx


@rx.page(route="/for-students", title="Nurse Reports")
def for_students_page() -> rx.Component:
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
            badge("Nursing Students", variant="neutral"),
            heading(
                "For Nursing Students",
                size="2xl",
                weight="bold",
                class_name="text-center",
            ),
            text(
                "NurseReports.org creates full hospital transparency so students can view detailed "
                "information on pay, culture, and experience. Before you walk into your first job, "
                "know and compare details across all your hospitals of interest.",
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
                "graduation-cap",
                "First Job Readiness",
                "Know the full picture of hospitals you're considering before accepting "
                "your first offer out of school.",
            ),
            _feature_card(
                "dollar-sign",
                "New Grad Pay",
                "Compare starting pay across hospitals and states so your first paycheck "
                "reflects the value you bring.",
            ),
            _feature_card(
                "heart-handshake",
                "Workplace Culture",
                "Find a hospital that invests in new graduates — one that builds your career "
                "rather than burning you out.",
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
                "Hospitals may make it seem like it's new graduates who should be thankful for "
                "the opportunity to work, but the reality is that new graduates are an incredible "
                "resource. Within a year of practicing, the hospital can develop a nurse to perform "
                "many of the same nursing tasks as nurses who have more experience and get paid at "
                "higher rates. Often new graduates are expected to fill shortages in less popular "
                "assignments, making them valuable for hospitals to cover areas with higher turnover "
                "and less interest.",
                class_name="leading-relaxed",
            ),
            text(
                "If you're a new graduate you have to realize that you are an asset to the hospital. "
                "As such you need to know the full situation of what you are walking into. Your first "
                "year is critical to establishing a connection to your job and the patients you serve. "
                "You shouldn't go to school for years just to come out and work at a hospital that "
                "destroys your hope for a fulfilling and balanced career.",
                class_name="leading-relaxed",
            ),
            text(
                "Although the hospital doesn't want to talk about it, pay is also extremely important "
                "to new graduates. Coming out of school with student loans, car payments, and housing "
                "costs after not being able to work a full time job can be incredibly overwhelming. No "
                "one wants to look at their first paycheck — work a grueling few months — and question "
                "what they got themselves into. We'll provide a comprehensive list of pay data alongside "
                "information on culture and experience to help you find a first job that balances pay, "
                "culture, and workplace satisfaction. The only thing we ask is that once you get hired "
                "you take five minutes to submit a report. We'll do the rest.",
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
