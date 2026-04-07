from ...components import (
    solid_button,
    outline_button,
    heading,
    text,
    badge,
    card,
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
        content(),
        footer(),
        class_name="flex-col items-center bg-white dark:bg-[#0a0a0a] w-full min-h-svh",
    )


def content() -> rx.Component:
    return rx.flex(
        hero(),
        stats_band(),
        features(),
        sponsors(),
        cta_band(),
        class_name="flex-col items-center w-full",
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

def hero() -> rx.Component:
    # Outer container is relative so the glow orb can be absolutely positioned.
    return rx.flex(
        # Decorative teal glow orb — sits behind all content.
        rx.box(
            class_name=(
                "absolute top-1/2 left-1/2 "
                "-translate-x-1/2 -translate-y-2/3 "
                "w-[900px] h-[500px] "
                "bg-teal-500/50 dark:bg-teal-600/20 "
                "blur-[140px] rounded-full "
                "pointer-events-none"
            ),
        ),
        # Content stack — sits in front of the glow.
        rx.flex(
            badge("Free · Anonymous · Nurse-powered"),
            heading(
                "Hospital reviews for nurses, by nurses.",
                class_name="font-bold text-5xl md:text-6xl text-center",
            ),
            text(
                "Find real pay data, staffing ratios, unit culture, and benefits "
                "— shared anonymously by nurses across the US.",
                class_name="text-center text-lg leading-relaxed max-w-md",
            ),
            rx.flex(
                solid_button(
                    "Get Started",
                    on_click=rx.redirect("/create-account"),
                    class_name="px-12 py-5 text-lg",
                ),
                outline_button(
                    "Learn More",
                    on_click=rx.redirect("/about-us"),
                    class_name="px-12 py-5 text-lg",
                ),
                class_name="flex-col md:flex-row items-center gap-3",
            ),
            class_name="relative flex-col items-center gap-8 w-full max-w-screen-sm z-10",
        ),
        class_name="relative flex-col items-center px-6 pt-28 pb-28 w-full",
    )


# ---------------------------------------------------------------------------
# Stats band
# ---------------------------------------------------------------------------

def stat_item(value: str, label: str) -> rx.Component:
    return rx.flex(
        heading(value, class_name="text-4xl"),
        text(label, class_name="text-base"),
        class_name="flex-col items-center gap-1 px-10 py-8 flex-1",
    )


def stats_band() -> rx.Component:
    return rx.flex(
        rx.flex(
            stat_item("500+", "Hospitals covered"),
            rx.divider(
                orientation="vertical",
                class_name="h-12 self-center border-neutral-300 dark:border-neutral-800",
            ),
            stat_item("50", "US states"),
            rx.divider(
                orientation="vertical",
                class_name="h-12 self-center border-neutral-300 dark:border-neutral-800",
            ),
            stat_item("$0", "Charged"),
            
            class_name="flex-row items-center justify-center w-full max-w-screen-md",
        ),
        class_name=(
            "flex-col items-center w-full "
            "border-y border-neutral-300 dark:border-white/[0.06] "
            "bg-teal-500/20 dark:bg-white/[0.03] "
            "backdrop-blur-md"
        ),
    )


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------

def feature_card(icon_tag: str, title: str, description: str) -> rx.Component:
    return rx.flex(
        card_header(
            icon(icon_tag, accent=True, class_name="h-5 w-5 shrink-0"),
            heading(title, class_name="text-lg font-semibold ml-3"),
        ),
        rx.flex(
            text(description, class_name="text-base leading-relaxed"),
            class_name="px-5 py-5",
        ),
        class_name=(
            "flex-col w-full "
            "bg-white/70 dark:bg-white/[0.04] "
            "border border-neutral-300 dark:border-neutral-800 "
            "rounded-2xl"
        ),
    )


def features() -> rx.Component:
    return rx.flex(
        rx.flex(
            heading(
                "Everything you need before your next assignment.",
                class_name="text-4xl font-bold text-center",
            ),
            text(
                "No more guessing. No more digging through social media.",
                class_name="text-center text-lg font-semibold",
            ),
            class_name="flex-col items-center gap-8 w-full max-w-screen-sm",
        ),
        rx.box(
            feature_card(
                "dollar-sign",
                "Pay & Benefits",
                "Compare base pay, differentials, sign-on bonuses, and benefits "
                "side-by-side across hospitals and states.",
            ),
            feature_card(
                "users",
                "Staffing Ratios",
                "See nurse-to-patient ratios by unit type so you know exactly "
                "what workload to expect on day one.",
            ),
            feature_card(
                "message-square",
                "Unit Culture",
                "Real accounts of management style, teamwork, and workplace "
                "environment — from nurses who've been there.",
            ),
            feature_card(
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
            "bg-neutral-300 dark:bg-neutral-800"
        ),
    )


def sponsors() -> rx.Component:
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
              .marquee-track:hover {
                animation-play-state: paused;
              }
              .marquee-fade {
                -webkit-mask-image: linear-gradient(
                  to right, transparent 0%, black 12%, black 88%, transparent 100%
                );
                mask-image: linear-gradient(
                  to right, transparent 0%, black 12%, black 88%, transparent 100%
                );
              }
            </style>
        """),
        rx.flex(
            text(
                "Made possible by our fantastic sponsors:",
                class_name="text-base text-neutral-400 dark:text-neutral-600 mb-8 text-center",
            ),
            rx.flex(
                rx.flex(
                    *logos,
                    *logos_dup,
                    class_name="marquee-track items-center",
                ),
                class_name="marquee-fade overflow-hidden w-full",
            ),
            class_name="flex-col items-center w-full max-w-screen-lg",
        ),
        class_name="flex-col items-center py-16 w-full",
    )



# ---------------------------------------------------------------------------
# CTA band
# ---------------------------------------------------------------------------

def cta_band() -> rx.Component:
    return rx.flex(
        rx.flex(
            heading(
                "Ready to make informed decisions?",
                class_name="text-2xl font-semibold text-center",
            ),
            text(
                "Join nurses sharing anonymous, honest hospital reviews.",
                class_name="text-center text-base",
            ),
            solid_button(
                "Create Account",
                on_click=rx.redirect("/create-account"),
                class_name="px-12 py-5 text-lg mt-2",
            ),
            class_name="flex-col items-center gap-4",
        ),
        class_name=(
            "flex-col items-center justify-center "
            "border-t border-neutral-300 dark:border-white/[0.06] "
            "bg-teal-500/20 dark:bg-white/[0.03] "
            "backdrop-blur-md "
            "py-20 px-6 w-full"
        ),
    )
