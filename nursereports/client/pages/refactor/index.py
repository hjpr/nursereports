"""
Landing page — emerald brand + cyan data accent.
Hero has an SVG fine vertical-wiggle texture layered under a soft emerald glow.
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

# ---------------------------------------------------------------------------
# SVG wiggle texture — injected once per page load via a <style> block.
# The pattern tiles 14 × 36 px; each tile is a single quadratic-bezier wiggle.
# ---------------------------------------------------------------------------
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
    route="/",
    title="Nurse Reports",
    on_load=BaseState.event_state_handle_sso_redirect,
)
def index_page() -> rx.Component:
    return rx.flex(
        _WIGGLE_STYLE,
        navbar(),
        _content(),
        footer(),
        class_name="flex-col items-center bg-neutral-50 dark:bg-[#07100a] w-full min-h-svh",
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
        # SVG wiggle texture layer
        rx.box(
            class_name=(
                "wiggle-texture "
                "absolute inset-0 "
                "opacity-80 dark:opacity-10 "
                "pointer-events-none"
            ),
        ),
        # Moth blob — softens the wiggle texture behind the text
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
        # Deep Lake glow behind content
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
                    color="emerald",
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
        heading(value, size="2xl", class_name="text-sky-600 dark:text-sky-400 font-mono"),
        heading(label, size='md'),
        class_name="flex-col items-center gap-1 px-10 py-8 flex-1",
    )


def _stats_band() -> rx.Component:
    return rx.flex(
        rx.flex(
            _stat_item("6,013", "Hospitals"),
            rx.divider(
                orientation="vertical",
                class_name="h-12 self-center border-neutral-300 dark:border-neutral-700",
            ),
            _stat_item("50", "States"),
            rx.divider(
                orientation="vertical",
                class_name="h-12 self-center border-neutral-300 dark:border-neutral-700",
            ),
            _stat_item("$0", "Charged"),
            class_name="flex-row items-center justify-center w-full max-w-screen-md",
        ),
        class_name=(
            "flex-col items-center w-full "
            "border-y border-neutral-300 dark:border-neutral-800/50 "
            "bg-white/50 dark:bg-white/[0.03] "
            "backdrop-blur-md"
        ),
    )


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------

def _feature_card(icon_tag: str, title: str, description: str) -> rx.Component:
    return rx.flex(
        # Card header with wiggle texture overlay
        rx.flex(
            rx.box(
                class_name=(
                    "wiggle-texture "
                    "absolute inset-0 "
                    "opacity-80 dark:opacity-10 "
                    "pointer-events-none"
                ),
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
        class_name="flex-col items-center gap-12 py-28 w-full bg-neutral-100/80 dark:bg-neutral-900/50",
    )


# ---------------------------------------------------------------------------
# Sponsors marquee
# ---------------------------------------------------------------------------

_SPONSOR_PLACEHOLDERS = list(range(8))


def _sponsor_logo(_: int) -> rx.Component:
    return rx.box(
        class_name=(
            "shrink-0 mx-8 h-12 w-12 rounded-xl "
            "bg-neutral-300/80 dark:bg-neutral-700/60"
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
        # Wiggle texture
        rx.box(
            class_name=(
                "wiggle-texture "
                "absolute inset-0 "
                "opacity-80 dark:opacity-10 "
                "pointer-events-none"
            ),
        ),
        # Moth blob — mirrors hero, softens wiggle behind text and button
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
