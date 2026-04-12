from ...components import (
    button,
    icon,
)
from ....states import BaseState, UserState, NavbarState

import reflex as rx


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def navbar() -> rx.Component:
    return rx.flex(
        _feedback_dialog(),
        rx.flex(
            # Left col: logo on desktop, empty spacer on mobile
            rx.flex(
                rx.flex(_logo(), class_name="hidden md:flex"),
                class_name="flex-1 flex-row items-center",
            ),
            # Center: full logo on mobile, nav links on desktop
            rx.flex(
                rx.flex(_logo(), class_name="flex md:hidden"),
                _nav_links(),
                class_name="flex-row items-center",
            ),
            # Right col: auth actions + hamburger on mobile
            rx.flex(
                _right_actions(),
                rx.flex(_mobile_trigger(), class_name="flex md:hidden"),
                class_name="flex-1 flex-row items-center justify-end gap-2",
            ),
            class_name="flex-row items-center w-full max-w-screen-xl px-6",
        ),
        class_name=(
            "sticky top-0 z-50 h-16 w-full "
            "flex-row items-center justify-center "
            "bg-white/80 dark:bg-[#07100a]/80 "
            "backdrop-blur-md "
            "border-b border-neutral-300 dark:border-neutral-800/50"
        ),
    )


# ---------------------------------------------------------------------------
# Logo
# ---------------------------------------------------------------------------

def _logo() -> rx.Component:
    return rx.flex(
        rx.icon(
            "square-activity",
            class_name="h-7 w-7 shrink-0 text-emerald-600 dark:text-emerald-500",
        ),
        rx.flex(
            rx.text(
                "Nurse",
                class_name="text-xl font-semibold text-emerald-600 dark:text-emerald-500 tracking-tight",
            ),
            rx.text(
                "Reports",
                class_name="text-xl font-semibold text-neutral-900 dark:text-neutral-100 tracking-tight",
            ),
            class_name="flex-row",
        ),
        on_click=rx.cond(
            UserState.user_claims_authenticated,
            rx.redirect("/dashboard"),
            rx.redirect("/"),
        ),
        class_name="flex-row items-center gap-2 cursor-pointer",
    )


# ---------------------------------------------------------------------------
# Desktop nav links (unauthenticated only)
# ---------------------------------------------------------------------------

_NAV_LINK = (
    "text-base font-medium "
    "text-neutral-500 dark:text-neutral-400 "
    "hover:text-neutral-900 dark:hover:text-neutral-100 "
    "transition-colors duration-150 "
    "cursor-pointer"
)


def _nav_links() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,
        rx.flex(),
        rx.flex(
            rx.link("Staff", href=f"{BaseState.host_address}/for-staff", class_name=_NAV_LINK),
            rx.link("Travelers", href=f"{BaseState.host_address}/for-travelers", class_name=_NAV_LINK),
            rx.link("Students", href=f"{BaseState.host_address}/for-students", class_name=_NAV_LINK),
            rx.link("Donate", href=f"{BaseState.host_address}/donate", class_name=f"{_NAV_LINK} text-emerald-600 dark:text-emerald-500 hover:text-emerald-700 dark:hover:text-emerald-400"),
            class_name="flex-row items-center gap-8 hidden md:flex",
        ),
    )


# ---------------------------------------------------------------------------
# Right-side actions
# ---------------------------------------------------------------------------

def _right_actions() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,
        # Authenticated: icon buttons
        rx.flex(
            rx.cond(
                ~UserState.user_needs_onboarding,
                rx.flex(
                    rx.tooltip(
                        button(
                            icon("search", class_name="h-5 w-5"),
                            variant='outline',
                            disabled=(BaseState.current_location == "/search/hospital"),
                            on_click=rx.redirect("/search/hospital"),
                            class_name="px-3.5 py-3",
                        ),
                        content="Search hospitals",
                        delay_duration=300,
                    ),
                    rx.tooltip(
                        button(
                            icon("layout-dashboard", class_name="h-5 w-5"),
                            variant='outline',
                            disabled=(BaseState.current_location == "/dashboard"),
                            on_click=rx.redirect("/dashboard"),
                            class_name="px-3.5 py-3",
                        ),
                        content="Dashboard",
                        delay_duration=300,
                    ),
                    rx.tooltip(
                        button(
                            icon("circle-user-round", class_name="h-5 w-5"),
                            variant='outline',
                            on_click=rx.redirect("/my-account"),
                            class_name="px-3.5 py-3",
                        ),
                        content="My account",
                        delay_duration=300,
                    ),
                    class_name="flex-row items-center gap-2 hidden md:flex",
                ),
            ),
        ),
        # Unauthenticated: Login
        rx.flex(
            button(
                "Login",
                variant='outline',
                on_click=rx.redirect("/login"),
                class_name="px-7 py-3 text-base",
            ),
            class_name="flex-row items-center gap-2 hidden md:flex",
        ),
    )


# ---------------------------------------------------------------------------
# Mobile hamburger + drawer
# ---------------------------------------------------------------------------

def _mobile_trigger() -> rx.Component:
    return rx.cond(
        UserState.user_claims_authenticated,
        _mobile_drawer_authenticated(),
        _mobile_drawer_public(),
    )


def _drawer_link(label: str, route: str) -> rx.Component:
    """Full-width tappable row for the mobile drawer."""
    return rx.flex(
        rx.text(
            label,
            class_name="text-base font-medium text-neutral-800 dark:text-neutral-200",
        ),
        on_click=rx.redirect(route),
        class_name=(
            "flex px-6 py-4 w-full cursor-pointer "
            "hover:bg-neutral-50 dark:hover:bg-white/[0.04] "
            "active:bg-neutral-100 dark:active:bg-white/[0.07] "
            "transition-colors duration-75"
        ),
    )


def _mobile_drawer_public() -> rx.Component:
    return rx.drawer.root(
        rx.drawer.trigger(
            button(
                icon("menu", class_name="h-4 w-4"),
                variant='outline',
                class_name="flex md:hidden",
            ),
        ),
        rx.drawer.overlay(class_name="backdrop-blur-sm"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.flex(
                    # Header row
                    rx.flex(
                        rx.flex(
                            rx.text(
                                "Nurse",
                                class_name="text-base font-semibold text-emerald-600 dark:text-emerald-500 tracking-tight",
                            ),
                            rx.text(
                                "Reports",
                                class_name="text-base font-semibold text-neutral-900 dark:text-neutral-100 tracking-tight",
                            ),
                            class_name="flex-row",
                        ),
                        rx.spacer(),
                        rx.drawer.close(
                            icon("x", class_name="h-5 w-5 cursor-pointer"),
                        ),
                        class_name="flex-row items-center px-6 py-5 w-full border-b border-neutral-300 dark:border-neutral-800/50",
                    ),
                    # Nav links
                    _drawer_link("Staff", "/for-staff"),
                    _drawer_link("Travelers", "/for-travelers"),
                    _drawer_link("Students", "/for-students"),
                    _drawer_link("Donate", "/donate"),
                    # Bottom actions
                    rx.flex(
                        button(
                            "Login",
                            variant='outline',
                            on_click=rx.redirect("/login"),
                            class_name="w-full",
                        ),
                        class_name="flex-col p-6 mt-auto w-full border-t border-neutral-300 dark:border-neutral-800/50",
                    ),
                    class_name=(
                        "flex-col h-full w-full "
                        "bg-neutral-50 dark:bg-[#07100a] "
                        "divide-y divide-neutral-200 dark:divide-neutral-800/50"
                    ),
                ),
                class_name="h-full w-full",
            ),
        ),
        direction="right",
    )


def _mobile_drawer_authenticated() -> rx.Component:
    return rx.cond(
        ~UserState.user_needs_onboarding,
        rx.drawer.root(
            rx.drawer.trigger(
                button(
                    icon("menu", class_name="h-4 w-4"),
                    variant='outline',
                    class_name="flex md:hidden",
                ),
            ),
            rx.drawer.overlay(class_name="backdrop-blur-sm"),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.flex(
                        # Header row
                        rx.flex(
                            rx.text(
                                "NurseReports",
                                class_name="text-base font-semibold text-neutral-900 dark:text-neutral-100 tracking-tight",
                            ),
                            rx.spacer(),
                            rx.drawer.close(
                                icon("x", class_name="h-5 w-5 cursor-pointer"),
                            ),
                            class_name="flex-row items-center px-6 py-5 w-full border-b border-neutral-300 dark:border-neutral-800/50",
                        ),
                        _drawer_link("Search Hospitals", "/search/hospital"),
                        _drawer_link("Dashboard", "/dashboard"),
                        _drawer_link("Donate", "/donate"),
                        # Logout at the bottom
                        rx.flex(
                            rx.flex(
                                icon("log-out", accent=True, class_name="h-4 w-4 shrink-0"),
                                rx.text(
                                    "Logout",
                                    class_name="text-base font-medium text-neutral-800 dark:text-neutral-200",
                                ),
                                class_name="flex-row items-center gap-3",
                            ),
                            on_click=BaseState.event_state_logout,
                            class_name=(
                                "flex px-6 py-4 mt-auto w-full cursor-pointer "
                                "hover:bg-neutral-50 dark:hover:bg-white/[0.04] "
                                "active:bg-neutral-100 dark:active:bg-white/[0.07] "
                                "transition-colors duration-75 "
                                "border-t border-neutral-300 dark:border-neutral-800/50"
                            ),
                        ),
                        class_name=(
                            "flex-col h-full w-full "
                            "bg-white dark:bg-[#07100a]"
                        ),
                    ),
                    class_name="h-full w-full",
                ),
            ),
            direction="right",
        ),
    )


# ---------------------------------------------------------------------------
# Feedback dialog (preserved for functionality)
# ---------------------------------------------------------------------------

def _feedback_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Provide feedback."),
            rx.form(
                rx.dialog.description(
                    rx.text_area(
                        name="feedback",
                        placeholder="Suggestions, improvements, or kudos?",
                        height="150px",
                        max_length=500,
                    ),
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            type="button",
                            variant="soft",
                            size="3",
                            radius="full",
                            on_click=NavbarState.set_show_feedback(False),
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Submit", type="submit", size="3", radius="full"),
                    ),
                    class_name="flex-row justify-end gap-3 mt-4",
                ),
                on_submit=NavbarState.event_state_submit_feedback,
            ),
        ),
        open=NavbarState.show_feedback,
    )
