from ..components.custom import spacer
from ...states import (
    BaseState,
    NavbarState
)

import reflex as rx


def navbar() -> rx.Component:
    return rx.flex(
        feedback_modal(),
        rx.flex(
            logo(),
            rx.flex(
                login_or_menu(),
                hamburger_mobile(),
                class_name="flex-row items-center space-x-2"
            ),
            class_name="flex-row items-center justify-between p-4 w-full max-w-screen-xl"
        ),
        class_name="flex-col items-center border justify-center sticky top-0 z-10 bg-white border-b-zinc-300 h-16 w-full"
    )

def logo() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.image(
                src="/vector/square-activity.svg",
                class_name="h-9 md:h-7 w-9 md:w-7"
            ),
            rx.flex(
                rx.text(
                    "Nurse",
                    on_click=rx.redirect("/"),
                    class_name="hidden md:flex text-2xl font-bold text-teal-700 cursor-pointer"
                ),
                rx.text(
                    "N",
                    class_name="flex md:hidden text-3xl font-bold text-teal-700 cursor-pointer"
                ),
                rx.text(
                    "Reports",
                    on_click=rx.redirect("/"),
                    class_name="hidden md:flex text-2xl font-bold text-zinc-700 cursor-pointer"
                ),
                rx.text(
                    "R",
                    on_click=rx.redirect("/"),
                    class_name="flex md:hidden text-3xl font-bold text-zinc-700 cursor-pointer"
                )
            ),
            class_name="flex-row items-center"
        ),
        links(),
        class_name="flex-row items-center space-x-8 justify-center"
    )


def links() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,
        
        # Displayed if user is authenticated.
        rx.flex(),

        # Displayed if user not authenticated.
        rx.flex(
            rx.link(
                "Staff",
                href="https://blog.nursereports.org/for-staff",
                class_name="cursor-pointer text-zinc-700"
            ),
            rx.link(
                "Travelers",
                href="https://blog.nursereports.org/for-travelers",
                class_name="cursor-pointer text-zinc-700"
            ),
            rx.link(
                "Students",
                href="https://blog.nursereports.org/for-students",
                class_name="cursor-pointer text-zinc-700"
            ),
            rx.flex(
                rx.link(
                    "Donate",
                    href=f"{BaseState.host_address}/donate",
                    class_name="cursor-pointer text-teal-700"
                ),
                class_name="flex-row items-center space-x-2 cursor-pointer"
            ),
            class_name="flex-row space-x-8 hidden lg:flex"
        )
    )


def login_or_menu() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,

        # Show menu if user is logged in.
        rx.box(
            rx.cond(
                BaseState.user_has_reported,
                rx.box(
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                rx.icon("menu"),
                                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg"
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(
                                "Search by Hospital",
                                on_click=rx.redirect(
                                    f"{BaseState.host_address}/search/hospital"
                                ),
                            ),
                            rx.menu.item(
                                "Search by State",
                                on_click=rx.redirect(
                                    f"{BaseState.host_address}/search/state"
                                ),
                            ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Dashboard",
                                on_click=rx.redirect(f"{BaseState.host_address}/dashboard"),
                            ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Donate",
                                on_click=rx.redirect(f"{BaseState.host_address}/donate"),
                            ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Logout",
                                on_click=rx.redirect(
                                    f"{BaseState.host_address}/logout/user"
                                ),
                            ),
                        ),
                    ),
                    cursor="pointer",
                ),
                rx.box(
                    rx.menu.root(
                        rx.menu.trigger(rx.icon("menu", color="teal")),
                        rx.menu.content(
                            rx.menu.item(
                                "Logout",
                                on_click=rx.redirect(
                                    f"{BaseState.host_address}/logout/user"
                                ),
                            )
                        ),
                    ),
                    cursor="pointer",
                ),
            ),
            class_name="hidden md:flex"
        ),

        # Show login button if user not logged in.
        rx.box(
            rx.button(
                "Login",
                on_click=rx.redirect("/login"),
                class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg cursor-pointer",
            ),
        )
    )


def hamburger_mobile() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,
        rx.cond(
            BaseState.user_has_reported,
            auth_report_hamburger_mobile(),
            auth_no_report_hamburger_mobile(),
        ),
        unauth_hamburger_mobile(),
    )


def auth_report_hamburger_mobile() -> rx.Component:
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(
                    rx.icon("menu"),
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg"
                )
            ),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.flex(
                        rx.flex(
                            rx.heading("Nurse Reports"),
                            rx.drawer.close(rx.icon("X", cursor="pointer")),
                            width="100%",
                            padding="30px 36px 30px 36px",
                            align_items="center",
                            justify_content="space-between",
                        ),
                        rx.flex(
                            rx.link(
                                "Search by Hospital",
                                href=f"{BaseState.host_address}/search/hospital",
                                cursor="pointer",
                            ),
                            rx.divider(),
                            rx.link(
                                "Search by State",
                                href=f"{BaseState.host_address}/search/state",
                                cursor="pointer",
                            ),
                            rx.divider(),
                            rx.link(
                                "Dashboard",
                                href=f"{BaseState.host_address}/dashboard",
                                cursor="pointer",
                            ),
                            rx.divider(),
                            rx.flex(
                                rx.link(
                                    "Donate",
                                    href=f"{BaseState.host_address}/donate",
                                    cursor="pointer",
                                ),
                                rx.icon("hand-coins", color="teal", size=18),
                                gap="12px",
                                align_items="center",
                            ),
                            rx.divider(),
                            rx.link(
                                "Logout",
                                on_click=BaseState.event_state_logout
                            ),
                            flex_direction="column",
                            width="100%",
                            gap="24px",
                            padding="30px 36px 30px 36px",
                            align_items="start",
                        ),
                        width="100%",
                        flex_direction="column",
                    ),
                    height="100%",
                    width="100%",
                    gap="36px",
                    background_color="#FFF",
                )
            ),
            direction="top",
        ),
        class_name="flex md:hidden"
    )


def auth_no_report_hamburger_mobile() -> rx.Component:
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(
                    rx.icon("menu"),
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg"
                )
            ),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.flex(
                        rx.flex(
                            rx.heading("Nurse Reports"),
                            rx.drawer.close(rx.icon("X", cursor="pointer")),
                            width="100%",
                            padding="30px 36px 30px 36px",
                            align_items="center",
                            justify_content="space-between",
                        ),
                        rx.flex(
                            rx.link(
                                "Log out",
                                href=f"{BaseState.host_address}/logout/user",
                                cursor="pointer",
                            ),
                        ),
                    )
                )
            ),
            direction="top",
        ),
        display=["block", "block", "block", "none", "none"],
    )


def unauth_hamburger_mobile() -> rx.Component:
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(
                rx.button(
                    rx.icon("menu", class_name="h-5 w-5"),
                    class_name="bg-transparent text-zinc-700 border border-solid border-zinc-300 shadow-lg"
                )
            ),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.flex(
                        rx.flex(
                            rx.heading("Nurse Reports"),
                            rx.drawer.close(rx.icon("X", cursor="pointer")),
                            width="100%",
                            padding="30px 36px 30px 36px",
                            align_items="center",
                            justify_content="space-between",
                        ),
                        rx.flex(
                            rx.link(
                                "Staff",
                                href="https://blog.nursereports.org/for-staff",
                                cursor="pointer",
                            ),
                            rx.divider(),
                            rx.link(
                                "Travelers",
                                href="https://blog.nursereports.org/for-travelers",
                                cursor="pointer",
                            ),
                            rx.divider(),
                            rx.link(
                                "Students",
                                href="https://blog.nursereports.org/for-students",
                                cursor="pointer",
                            ),
                            rx.divider(),
                            rx.flex(
                                rx.link(
                                    "Donate",
                                    href="https://nursereports.org/donate",
                                    cursor="pointer",
                                ),
                                rx.icon("sparkles", color="teal", size=18),
                                gap="12px",
                                align_items="center",
                            ),
                            rx.divider(),
                            rx.link(
                                "Login",
                                on_click=rx.redirect("/login"),
                            ),
                            flex_direction="column",
                            width="100%",
                            gap="24px",
                            padding="30px 36px 30px 36px",
                            align_items="start",
                        ),
                        width="100%",
                        flex_direction="column",
                    ),
                    height="100%",
                    width="100%",
                    gap="36px",
                    background_color="#FFF",
                )
            ),
            direction="top",
        ),
        class_name="flex lg:hidden"
    )

def feedback_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Provide feedback."),
            rx.form(
                rx.dialog.description(
                    rx.text_area(
                        name="feedback",
                        placeholder="What can we improve?",
                        height="150px",
                        max_length=500,
                    )
                ),
                spacer(height="16px"),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            type="button",
                            variant="soft",
                            size="3",
                            radius="full",
                            on_click=NavbarState.set_show_feedback(False),
                        )
                    ),
                    rx.dialog.close(
                        rx.button("Submit", type="submit", size="3", radius="full")
                    ),
                    spacing="3",
                    justify="end",
                ),
                spacer(height="4px"),
                rx.cond(
                    NavbarState.error_message,
                    rx.callout(
                        NavbarState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                        margin_top="12px",
                    ),
                ),
                on_submit=NavbarState.event_state_submit_feedback,
            ),
        ),
        open=NavbarState.show_feedback,
    )