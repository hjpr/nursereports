from ..components import button, heading, text, badge, icon
from .navbar import navbar
from .footer import footer

import reflex as rx


@rx.page(route="/for-staff", title="Nurse Reports")
def for_staff_page() -> rx.Component:
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
            badge("Staff Nurses", variant="neutral"),
            heading(
                "For Staff Nurses",
                size="2xl",
                weight="bold",
                class_name="text-center",
            ),
            text(
                "NurseReports.org creates full hospital transparency by allowing staff nurses "
                "to share detailed information on pay, culture, and experience. Get the information "
                "you need to make confident career decisions.",
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
                "dollar-sign",
                "Pay Transparency",
                "Compare base pay, differentials, and benefits across hospitals and regions "
                "to understand the fair market value of your labor.",
            ),
            _feature_card(
                "users",
                "Staffing Ratios",
                "See real nurse-to-patient ratios by unit so you know the workload "
                "before you sign.",
            ),
            _feature_card(
                "message-square",
                "Culture & Management",
                "Real accounts from nurses who've worked there — management style, teamwork, "
                "and what the environment is actually like.",
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
                "Staff nurses are the core component of any hospital institution. Our roles spread "
                "across so many different areas that it's harder to think about what nurses aren't "
                "involved in than what we are. Nurses are essential to both in-hospital care, and "
                "continuing care after discharge. We provide direct patient-facing care, but also "
                "we're in the background ensuring that all the pieces of this complicated system "
                "are organized.",
                class_name="leading-relaxed",
            ),
            text(
                "The way that nurses get paid is similarly diverse. Nurses get paid in the form of "
                "full-time, part-time, hourly, weekly, bi-weekly, and yearly wages. That diversity "
                "of pay along with the varying cost of living can make it extremely difficult to "
                "decipher not only the environment of nursing pay, but also the fair market value "
                "of our labor.",
                class_name="leading-relaxed",
            ),
            text(
                "A major focus of NurseReports.org is not just as a simple repository of pay "
                "information. NurseReports.org condenses, compares, and organizes pay data provided "
                "by nurses from across the US to help you understand what's fair regardless of "
                "where you are practicing.",
                class_name="leading-relaxed",
            ),
            text(
                "Pay transparency doesn't go far enough in our opinion. We are building a powerful "
                "platform using your data and our tools so that in one or two clicks you can make "
                "impactful decisions that lead to competitive wages, solid benefits, and bring actual "
                "accountability to hospital systems nationwide. All of this starts with you taking "
                "five minutes to submit a simple report. We'll do the rest.",
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
