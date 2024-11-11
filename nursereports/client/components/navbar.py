from ..components.custom import spacer
from reflex.style import toggle_color_mode
from ...states import (
    BaseState,
    LoginState,
    NavbarState
)

import reflex as rx


def navbar() -> rx.Component:
    return rx.flex(
        feedback_modal(),
        rx.flex(
            rx.flex(
                rx.image(
                    src="/vector/square-activity.svg",
                    class_name="h-5.5 w-5.5 mb-0.5 mr-1"
                ),
                rx.heading(
                    "Nurse Reports",
                    on_click=rx.redirect("/"),
                    color_scheme="teal",
                    size="6",
                    cursor="pointer",
                ),
                class_name="flex-row justify-center"
            ),
            links(),
            hamburger_mobile(),
            sign_in_or_menu(),
            flex_direction="row",
            align_items="center",
            justify_content="space-between",
            width="100%",
            max_width="1000px",
            padding="0px 36px 0px 36px",
        ),
        bg="white",
        width="100%",
        align_items="center",
        justify_content="center",
        height="64px",
        border_bottom="1px solid #E2E8F0",
        position="sticky",
        top="0px",
        z_index="5",
    )


def links() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,
        auth_links(),
        unauth_links()
    )


def unauth_links() -> rx.Component:
    return rx.flex(
        rx.link(
            "Staff", href="https://blog.nursereports.org/for-staff", cursor="pointer"
        ),
        rx.link(
            "Travelers",
            href="https://blog.nursereports.org/for-travelers",
            cursor="pointer",
        ),
        rx.link(
            "Students",
            href="https://blog.nursereports.org/for-students",
            cursor="pointer",
        ),
        rx.flex(
            rx.link(
                "Donate", href=f"{BaseState.host_address}/donate", cursor="pointer"
            ),
            rx.icon("hand-coins", color="teal", size=18),
            flex_direction="row",
            gap="8px",
            align_items="center",
            justify_content="center",
            cursor="pointer",
        ),
        flex_direction="row",
        gap="24px",
        display=["none", "none", "none", "flex", "flex"],
    )


def auth_links() -> rx.Component:
    return rx.flex()


def sign_in_or_menu() -> rx.Component:
    return rx.cond(
        BaseState.user_claims_authenticated,
        menu(),
        login()
    )


def login() -> rx.Component:
    return rx.box(
        rx.link(
            "Login",
            class_name="cursor-pointer",
            on_click=[
                LoginState.set_current_tab("login"),
                rx.redirect("/login"),
            ]
        ),
        display=["none", "none", "none", "inline", "inline"],
        margin="0 0 0 60px",
    )


def menu() -> rx.Component:
    return rx.box(
        rx.cond(
            BaseState.user_has_reported,
            rx.box(
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", color="teal")),
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
        display=["none", "none", "none", "inline", "inline"],
        margin="0 0 0 60px",
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
            rx.drawer.trigger(rx.icon("menu", color="teal", cursor="pointer")),
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
        display=["block", "block", "block", "none", "none"],
    )


def auth_no_report_hamburger_mobile() -> rx.Component:
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(rx.icon("menu", color="teal", cursor="pointer")),
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
            rx.drawer.trigger(rx.icon("menu", color="teal", cursor="pointer")),
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
                                on_click=[
                                    LoginState.set_current_tab("login"),
                                    rx.redirect("/login"),
                                ]
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
        display=["block", "block", "block", "none", "none"],
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