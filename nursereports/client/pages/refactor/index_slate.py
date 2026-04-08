"""
Slate variant — clean slate & indigo.
A restrained, professional palette with a deep indigo glow and crisp borders.
"""
from ...components import (
    button,
    heading,
    text,
    badge,
    card_header,
    icon,
)
from .navbar import navbar
from .footer import footer
from ....states import BaseState

import reflex as rx


@rx.page(
    route="/",
    title="Nurse Reports",
    on_load=BaseState.event_state_handle_sso_redirect,
)
def index_page() -> rx.Component:
    return rx.flex(
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-slate-50 dark:bg-[#090b12] w-full min-h-svh",
    )


def _content() -> rx.Component:
    return rx.flex(
        _hero(),
        _stats_band(),
        _features(),
        _sponsors(),
        _cta_band(),
        class_name="flex-col items-center w-full",
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

def _hero() -> rx.Component:
    return rx.flex(
        # Wide, low indigo glow — more of a horizon haze than a centered orb
        rx.box(
            class_name=(
                "absolute bottom-0 left-1/2 "
                "-translate-x-1/2 translate-y-1/4 "
                "w-[1100px] h-[300px] "
                "bg-indigo-500/25 dark:bg-indigo-700/15 "
                "blur-[120px] rounded-full "
                "pointer-events-none"
            ),
        ),
        # Smaller centered accent orb
        rx.box(
            class_name=(
                "absolute top-1/3 left-1/2 "
                "-translate-x-1/2 -translate-y-1/2 "
                "w-[400px] h-[200px] "
                "bg-blue-400/20 dark:bg-blue-600/10 "
                "blur-[80px] rounded-full "
                "pointer-events-none"
            ),
        ),
        # Content
        rx.flex(
            badge("Free · Anonymous · Nurse-powered", variant="neutral"),
            heading(
                "Hospital reviews for nurses, by nurses.",
                size="3xl",
                weight="bold",
                class_name="text-center",
            ),
            text(
                "Find real pay data, staffing ratios, unit culture, and benefits "
                "— shared anonymously by nurses across the US.",
                size="lg",
                class_name="text-center leading-relaxed max-w-md",
            ),
            rx.flex(
                button(
                    "Get Started",
                    on_click=rx.redirect("/create-account"),
                    color="indigo",
                    size="xl",
                ),
                button(
                    "Learn More",
                    on_click=rx.redirect("/about-us"),
                    variant="outline",
                    size="xl",
                ),
                class_name="flex-col md:flex-row items-center gap-3",
            ),
            class_name="relative flex-col items-center gap-8 w-full max-w-screen-sm z-10",
        ),
        class_name="relative flex-col items-center px-6 pt-28 pb-28 w-full overflow-hidden",
    )


# ---------------------------------------------------------------------------
# Stats band
# ---------------------------------------------------------------------------

def _stat_item(value: str, label: str) -> rx.Component:
    return rx.flex(
        heading(value, size="2xl"),
        text(label),
        class_name="flex-col items-center gap-1 px-10 py-8 flex-1",
    )


def _stats_band() -> rx.Component:
    return rx.flex(
        rx.flex(
            _stat_item("500+", "Hospitals covered"),
            rx.divider(
                orientation="vertical",
                class_name="h-12 self-center border-slate-300 dark:border-slate-700",
            ),
            _stat_item("50", "US states"),
            rx.divider(
                orientation="vertical",
                class_name="h-12 self-center border-slate-300 dark:border-slate-700",
            ),
            _stat_item("$0", "Charged"),
            class_name="flex-row items-center justify-center w-full max-w-screen-md",
        ),
        class_name=(
            "flex-col items-center w-full "
            "border-y border-slate-200 dark:border-slate-800 "
            "bg-indigo-500/8 dark:bg-slate-800/40 "
            "backdrop-blur-md"
        ),
    )


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------

def _feature_card(icon_tag: str, title: str, description: str) -> rx.Component:
    return rx.flex(
        card_header(
            icon(icon_tag, accent=True, class_name="h-5 w-5 shrink-0"),
            heading(title, size="sm", weight="semibold", class_name="ml-3"),
        ),
        rx.flex(
            text(description, class_name="leading-relaxed"),
            class_name="px-5 py-5",
        ),
        class_name=(
            "flex-col w-full "
            "bg-white dark:bg-slate-900/60 "
            "border border-slate-200 dark:border-slate-800 "
            "rounded-2xl"
        ),
    )


def _features() -> rx.Component:
    return rx.flex(
        rx.flex(
            heading(
                "Everything you need before your next assignment.",
                size="2xl",
                weight="bold",
                class_name="text-center",
            ),
            text(
                "No more guessing. No more digging through social media.",
                size="lg",
                weight="semibold",
                class_name="text-center",
            ),
            class_name="flex-col items-center gap-8 w-full max-w-screen-sm",
        ),
        rx.box(
            _feature_card(
                "dollar-sign",
                "Pay & Benefits",
                "Compare base pay, differentials, sign-on bonuses, and benefits "
                "side-by-side across hospitals and states.",
            ),
            _feature_card(
                "users",
                "Staffing Ratios",
                "See nurse-to-patient ratios by unit type so you know exactly "
                "what workload to expect on day one.",
            ),
            _feature_card(
                "message-square",
                "Unit Culture",
                "Real accounts of management style, teamwork, and workplace "
                "environment — from nurses who've been there.",
            ),
            _feature_card(
                "bar-chart-2",
                "Rankings & Analytics",
                "Rank hospitals by pay or culture score. Zoom into a single "
                "unit or pull back and compare entire states.",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-screen-lg px-6",
        ),
        class_name="flex-col items-center gap-12 py-28 w-full",
    )


# ---------------------------------------------------------------------------
# Sponsors marquee
# ---------------------------------------------------------------------------

_SPONSOR_PLACEHOLDERS = list(range(8))


def _sponsor_logo(_: int) -> rx.Component:
    return rx.box(
        class_name=(
            "shrink-0 mx-8 h-12 w-12 rounded-xl "
            "bg-slate-200 dark:bg-slate-800"
        ),
    )


def _sponsors() -> rx.Component:
    logos = [_sponsor_logo(n) for n in _SPONSOR_PLACEHOLDERS]
    logos_dup = [_sponsor_logo(n) for n in _SPONSOR_PLACEHOLDERS]

    return rx.flex(
        rx.html("""
            <style>
              @keyframes marquee-scroll {
                from { transform: translateX(0); }
                to   { transform: translateX(-50%); }
              }
              .marquee-track {
                animation: marquee-scroll 56s linear infinite;
                display: flex;
                width: max-content;
              }
              .marquee-track:hover { animation-play-state: paused; }
              .marquee-fade {
                -webkit-mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
                mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
              }
            </style>
        """),
        rx.flex(
            text("Made possible by our fantastic sponsors:", color="neutral-400", class_name="mb-8 text-center"),
            rx.flex(
                rx.flex(*logos, *logos_dup, class_name="marquee-track items-center"),
                class_name="marquee-fade overflow-hidden w-full",
            ),
            class_name="flex-col items-center w-full max-w-screen-lg",
        ),
        class_name="flex-col items-center py-16 w-full",
    )


# ---------------------------------------------------------------------------
# CTA band
# ---------------------------------------------------------------------------

def _cta_band() -> rx.Component:
    return rx.flex(
        rx.flex(
            heading(
                "Ready to make informed decisions?",
                size="lg",
                weight="semibold",
                class_name="text-center",
            ),
            text("Join nurses sharing anonymous, honest hospital reviews.", class_name="text-center"),
            button(
                "Create Account",
                on_click=rx.redirect("/create-account"),
                color="indigo",
                size="xl",
            ),
            class_name="flex-col items-center gap-4",
        ),
        class_name=(
            "flex-col items-center justify-center "
            "border-t border-slate-200 dark:border-slate-800 "
            "bg-indigo-500/8 dark:bg-slate-800/40 "
            "backdrop-blur-md "
            "py-20 px-6 w-full"
        ),
    )
