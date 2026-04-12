from ...components import icon, link
from ....states import BaseState, UserState

import reflex as rx


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def footer() -> rx.Component:
    return rx.flex(
        rx.flex(
            _main_grid(),
            _bottom_bar(),
            class_name="flex-col w-full max-w-screen-xl px-6",
        ),
        class_name=(
            "flex-col items-center "
            "border-t border-neutral-300 dark:border-neutral-800/50 "
            "bg-gradient-to-b from-emerald-500/20 to-transparent "
            "dark:from-transparent dark:to-black/60 "
            "py-16 w-full"
        ),
    )


# ---------------------------------------------------------------------------
# Main grid: logo col + link columns
# ---------------------------------------------------------------------------

def _main_grid() -> rx.Component:
    return rx.flex(
        _logo_col(),
        rx.flex(
            _link_col(
                "Explore",
                rx.cond(
                    ~UserState.user_claims_authenticated,
                    rx.flex(
                        _footer_link("Staff", f"{BaseState.host_address}/for-staff"),
                        _footer_link("Travelers", f"{BaseState.host_address}/for-travelers"),
                        _footer_link("Students", f"{BaseState.host_address}/for-students"),
                        class_name="flex-col gap-3",
                    ),
                    rx.flex(),
                ),
            ),
            _link_col(
                "Company",
                rx.flex(
                    _footer_link("About Us", f"{BaseState.host_address}/about-us"),
                    _footer_link("Roadmap", f"{BaseState.host_address}/roadmap"),
                    _footer_link("Contact Us", f"{BaseState.host_address}/contact-us"),
                    _footer_link("Donate", f"{BaseState.host_address}/donate"),
                    class_name="flex-col gap-3",
                ),
            ),
            _link_col(
                "Legal",
                rx.flex(
                    _footer_link("Privacy Policy", f"{BaseState.host_address}/policy-privacy"),
                    _footer_link("AI Policy", f"{BaseState.host_address}/policy-ai"),
                    class_name="flex-col gap-3",
                ),
            ),
            class_name="flex-row flex-wrap gap-12",
        ),
        class_name="flex-col md:flex-row justify-between gap-12 pb-12 border-b border-neutral-300 dark:border-neutral-800/50 w-full",
    )


def _logo_col() -> rx.Component:
    return rx.flex(
        # Logo
        rx.flex(
            rx.icon("square-activity", class_name="h-7 w-7 shrink-0 text-emerald-600 dark:text-emerald-500"),
            rx.text(
                "Nurse",
                class_name="text-xl font-semibold text-emerald-600 dark:text-emerald-500 tracking-tight",
            ),
            rx.text(
                "Reports",
                class_name="text-xl font-semibold text-neutral-900 dark:text-neutral-100 tracking-tight",
            ),
            on_click=rx.redirect("/"),
            class_name="flex-row items-center gap-2 cursor-pointer",
        ),
        # Tagline
        rx.text(
            "Hospital reviews for nurses, by nurses.",
            class_name="text-sm text-neutral-500 dark:text-neutral-500 max-w-[220px] leading-relaxed",
        ),
        # Social icons
        rx.flex(
            _social_icon("linkedin", "https://linkedin.com"),
            _social_icon("twitter", "https://twitter.com"),
            _social_icon("github", "https://github.com"),
            class_name="flex-row items-center gap-4",
        ),
        class_name="flex-col gap-5",
    )


def _social_icon(tag: str, href: str) -> rx.Component:
    return rx.link(
        icon(tag, muted=True, class_name="h-5 w-5 hover:text-neutral-700 dark:hover:text-neutral-300 transition-colors duration-150"),
        href=href,
    )


def _link_col(heading: str, children: rx.Component) -> rx.Component:
    return rx.flex(
        rx.text(
            heading,
            class_name=(
                "text-xs font-semibold uppercase tracking-widest "
                "text-neutral-400 dark:text-neutral-600 mb-1"
            ),
        ),
        children,
        class_name="flex-col gap-4",
    )


def _footer_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        class_name=(
            "text-sm "
            "text-neutral-600 dark:text-neutral-400 "
            "hover:text-neutral-900 dark:hover:text-neutral-100 "
            "transition-colors duration-150"
        ),
    )


# ---------------------------------------------------------------------------
# Bottom bar: copyright + color mode toggle
# ---------------------------------------------------------------------------

def _bottom_bar() -> rx.Component:
    return rx.flex(
        rx.text(
            "© 2026 Nurse Reports",
            class_name="text-sm text-neutral-400 dark:text-neutral-600",
        ),
        rx.spacer(),
        _color_mode_toggle(),
        class_name="flex-row items-center pt-8 w-full",
    )


def _color_mode_toggle() -> rx.Component:
    return rx.flex(
        rx.color_mode_cond(
            # Light mode — show moon to switch to dark
            light=rx.flex(
                icon("moon", muted=True, class_name="h-4 w-4"),
                rx.text("Dark", class_name="text-sm text-neutral-400"),
                class_name="flex-row items-center gap-2",
            ),
            # Dark mode — show sun to switch to light
            dark=rx.flex(
                icon("sun", muted=True, class_name="h-4 w-4"),
                rx.text("Light", class_name="text-sm text-neutral-600"),
                class_name="flex-row items-center gap-2",
            ),
        ),
        on_click=rx.toggle_color_mode,
        class_name=(
            "flex-row items-center gap-2 px-3 py-1.5 rounded-full cursor-pointer "
            "ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50 "
            "hover:bg-neutral-100 dark:hover:bg-white/[0.05] "
            "transition-colors duration-150"
        ),
    )
