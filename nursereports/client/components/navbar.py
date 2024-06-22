from ..components.custom import spacer
from ...states import BaseState
from ...states import NavbarState

import reflex as rx


def navbar() -> rx.Component:
    return rx.flex(
        alert_modal(),
        feedback_modal(),
        login_modal(),
        rx.flex(
            rx.flex(
                rx.image(
                    src="/vector/square-activity.svg",
                    height="22px",
                    width="22px",
                    margin="4px 0 0 0",
                ),
                rx.heading(
                    "Nurse Reports",
                    on_click=rx.redirect("/"),
                    color_scheme="teal",
                    size="6",
                    cursor="pointer",
                ),
                flex_direction="row",
                gap="6px",
                justify_content="center",
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
        width="100%",
        align_items="center",
        justify_content="center",
        height=["80px", "80px", "96px", "96px" "96px"],
        z_index="5",
    )


def links() -> rx.Component:
    return rx.cond(BaseState.user_is_authenticated, auth_links(), unauth_links())


def unauth_links() -> rx.Component:
    return rx.flex(
        rx.link(
            "Staff",
            href="https://blog.nursereports.org/for-staff",
            cursor='pointer'
        ),
        rx.link(
            "Travelers",
            href="https://blog.nursereports.org/for-travelers",
            cursor='pointer'
        ),
        rx.link(
            "Students",
            href="https://blog.nursereports.org/for-students",
            cursor='pointer'
        ),
        rx.flex(
            rx.link(
                "Donate",
                href=f"{BaseState.host_address}/donate",
                cursor="pointer"
                ),
            rx.icon("hand-coins", color="teal", size=18),
            flex_direction="row",
            gap="8px",
            align_items="center",
            justify_content="center",
            cursor='pointer'
        ),
        flex_direction="row",
        gap="24px",
        display=["none", "none", "none", "flex", "flex"],
    )


def auth_links() -> rx.Component:
    return rx.flex()


def sign_in_or_menu() -> rx.Component:
    return rx.cond(
        BaseState.user_is_authenticated,
        menu(),
        signin()
        )


def signin() -> rx.Component:
    return rx.box(
        rx.link(
            "Sign In",
            on_click=NavbarState.event_state_navbar_pressed_sign_in,
            cursor="pointer"
            ),
        display=["none", "none", "none", "inline", "inline"],
        margin="0 0 0 60px",
    )


def menu() -> rx.Component:
    return rx.box(
        rx.cond(
            BaseState.user_has_reported,
            rx.flex(
                rx.box(
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon("menu", color="teal")
                        ),
                        rx.menu.content(
                            rx.menu.item(
                                "Search by Hospital",
                                on_click=rx.redirect(f"{BaseState.host_address}/search/hospital")
                                ),
                            rx.menu.item(
                                "Search by State",
                                on_click=rx.redirect(f"{BaseState.host_address}/search/state")
                                ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Dashboard",
                                on_click=rx.redirect(f"{BaseState.host_address}/dashboard")
                                ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Donate",
                                on_click=rx.redirect(f"{BaseState.host_address}/donate")
                                ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Logout",
                                on_click=rx.redirect(f"{BaseState.host_address}/logout/user")
                                )
                        )
                    ),
                    cursor="pointer"
                )
            ),
            rx.box(
                rx.icon(
                    "menu",
                    color="teal",
                    on_click=NavbarState.set_alert_message(
                        "Submit a report before accessing the dashboard."
                    )
                ),
                cursor="pointer"
            )
        ),
        display=["none", "none", "none", "inline", "inline"],
        margin="0 0 0 60px",
    )


def hamburger_mobile() -> rx.Component:
    return rx.cond(
        BaseState.user_is_authenticated,
        rx.cond(
            BaseState.user_has_reported,
            auth_report_hamburger_mobile(),
            auth_no_report_hamburger_mobile()
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
                                cursor="pointer"
                            ),
                            rx.divider(),
                            rx.link(
                                "Search by State",
                                href=f"{BaseState.host_address}/search/state",
                                cursor="pointer"
                            ),
                            rx.divider(),
                            rx.link(
                                "Dashboard",
                                href=f"{BaseState.host_address}/dashboard",
                                cursor="pointer"
                                ),
                            rx.divider(),
                            rx.flex(
                                rx.link(
                                    "Donate",
                                    href=f"{BaseState.host_address}/donate",
                                    cursor="pointer"
                                    ),
                                rx.icon("hand-coins", color="teal", size=18),
                                gap="12px",
                                align_items="center",
                            ),
                            rx.divider(),
                            rx.link("Logout",
                                    href=f"{BaseState.host_address}/logout/user"
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
                                cursor="pointer"
                            ),
                        )
                    )
                )
            ),
            direction="top"
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
                                cursor="pointer"
                            ),
                            rx.divider(),
                            rx.link(
                                "Travelers",
                                href="https://blog.nursereports.org/for-travelers",
                                cursor="pointer"
                                ),
                            rx.divider(),
                            rx.link(
                                "Students",
                                href="https://blog.nursereports.org/for-students",
                                cursor="pointer"
                                ),
                            rx.divider(),
                            rx.flex(
                                rx.link(
                                    "Donate",
                                    href="https://nursereports.org/donate",
                                    cursor="pointer"
                                    ),
                                rx.icon("sparkles", color="teal", size=18),
                                gap="12px",
                                align_items="center",
                            ),
                            rx.divider(),
                            rx.link(
                                "Sign In",
                                on_click=NavbarState.event_state_navbar_pressed_sign_in,
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


def alert_modal() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Message"),
            rx.alert_dialog.description(NavbarState.alert_message),
            rx.flex(
                rx.alert_dialog.action(
                    rx.button(
                        "OK",
                        size="3",
                        radius="full",
                        on_click=NavbarState.set_alert_message(""),
                    )
                ),
                margin_top="16px",
                justify="end",
            ),
        ),
        open=NavbarState.show_alert_message,
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
                    NavbarState.error_feedback_message,
                    rx.callout(
                        NavbarState.error_feedback_message,
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


def login_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.flex(
                    rx.button(
                        rx.icon(tag="x"),
                        size="1",
                        variant="ghost",
                        on_click=NavbarState.event_state_toggle_login,
                    ),
                    justify="end",
                    width="100%",
                )
            ),
            rx.form(
                rx.flex(
                    rx.tabs.root(
                        rx.center(
                            rx.tabs.list(
                                rx.tabs.trigger(
                                    "Login",
                                    value="login",
                                    on_click=NavbarState.set_login_tab("login"),
                                ),
                                rx.tabs.trigger(
                                    "Create Account",
                                    value="create_account",
                                    on_click=NavbarState.set_login_tab(
                                        "create_account"
                                    ),
                                ),
                                size="2",
                            ),
                            width="100%",
                        ),
                        rx.tabs.content(
                            login_tab_login(),
                            value="login",
                        ),
                        rx.tabs.content(login_tab_account(), value="create_account"),
                        value=NavbarState.login_tab,
                        width="100%",
                    ),
                    justify="center",
                ),
                on_submit=NavbarState.event_state_login_modal_submit,
            ),
            max_width="400px",
            on_escape_key_down=NavbarState.set_show_login(False),
        ),
        open=NavbarState.show_login,
    )


def login_tab_login() -> rx.Component:
    return rx.flex(
        spacer(),
        rx.heading(
            "Login to your account", size="6", text_align="center", width="100%"
        ),
        rx.flex(
            rx.flex(
                rx.text("Email", size="2", padding="0 0 0 12px"),
                rx.input(
                    placeholder="Enter email",
                    name="login_email",
                    width="100%",
                    size="3",
                    radius="full",
                    required=True,
                ),
                flex_direction="column",
                width="100%",
            ),
            rx.flex(
                rx.text("Password", size="2", padding="0 0 0 12px"),
                rx.input(
                    placeholder="Enter password",
                    name="login_password",
                    type="password",
                    width="100%",
                    size="3",
                    radius="full",
                    required=True,
                ),
                flex_direction="column",
                width="100%",
            ),
            login_callout(),
            rx.button(
                "Login",
                width="100%",
                type="submit",
                size="3",
                radius="full",
                margin="20px 0 0 0",
            ),
            flex_direction="column",
            gap="24px",
            width="100%",
            justify_content="center",
            padding="0 48px 0 48px",
        ),
        rx.hstack(
            rx.divider(),
            rx.text("OR", size="2", padding="6px", white_space="nowrap"),
            rx.divider(),
            align="center",
            width="100%",
            padding="12px 0 0 0",
        ),
        rx.hstack(
            rx.image(
                src="/sso/google_sso.png",
                height="44px",
                cursor="pointer",
                on_click=NavbarState.event_state_login_with_sso("google"),
            ),
            rx.image(
                src="/sso/facebook_sso.png",
                height="44px",
                cursor="pointer",
                on_click=NavbarState.event_state_login_with_sso("facebook"),
            ),
            rx.image(
                src="/sso/linkedin_sso.png",
                height="44px",
                cursor="pointer",
                on_click=NavbarState.event_state_login_with_sso("linkedin_oidc"),
            ),
            width="100%",
            justify="center",
            gap="48px",
            padding="12px 0 12px 0",
        ),
        spacer(),
        width="100%",
        gap="24px",
        flex_direction="column",
    )


def login_callout() -> rx.Component:
    return rx.cond(
        NavbarState.error_sign_in_message,
        rx.callout(
            NavbarState.error_sign_in_message,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            margin="20px 0 0 0",
        ),
    )


def login_tab_account() -> rx.Component:
    return rx.flex(
        spacer(),
        rx.heading("Create new account", size="6", text_align="center", width="100%"),
        rx.flex(
            rx.flex(
                rx.text("Email", size="2", padding="0 0 0 12px"),
                rx.input(
                    placeholder="Enter email",
                    name="create_account_email",
                    width="100%",
                    radius="full",
                    size="3",
                    required=True,
                ),
                flex_direction="column",
                width="100%",
            ),
            rx.flex(
                rx.flex(
                    rx.text("Password", size="2", padding="0 0 0 12px"),
                    rx.input(
                        placeholder="Enter password",
                        name="create_account_password",
                        type="password",
                        width="100%",
                        size="3",
                        radius="full",
                        required=True,
                    ),
                    flex_direction="column",
                    width="100%",
                ),
                rx.flex(
                    rx.text("Confirm password", size="2", padding="0 0 0 12px"),
                    rx.input(
                        placeholder="Re-enter password",
                        name="create_account_password_confirm",
                        type="password",
                        width="100%",
                        size="3",
                        radius="full",
                        required=True,
                    ),
                    flex_direction="column",
                    width="100%",
                ),
                flex_direction="column",
                gap="24px",
            ),
            create_account_callout(),
            rx.center(
                rx.button(
                    "Create account",
                    width="100%",
                    type="submit",
                    size="3",
                    radius="full",
                    margin="20px 0 0 0",
                ),
                width="100%",
            ),
            flex_direction="column",
            width="100%",
            gap="24px",
            padding="0 48px 0 48px",
        ),
        spacer(),
        rx.center(
            rx.flex(
                rx.link("Privacy Policy", size="2"),
                rx.divider(orientation="vertical"),
                rx.link("AI Policy", size="2"),
                flex_direction="row",
                width="100%",
                gap="24px",
                justify_content="center",
            )
        ),
        spacer(),
        spacer(),
        width="100%",
        gap="24px",
        flex_direction="column",
    )


def create_account_callout() -> rx.Component:
    return rx.cond(
        NavbarState.error_create_account_message,
        rx.callout(
            NavbarState.error_create_account_message,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            margin="20px 0 0 0",
        ),
    )
