
from ...states import BaseState, LoginState

import reflex as rx

@rx.page(
    route="/login",
    title="Nurse Reports",
    on_load=BaseState.event_state_auth_flow
)
def login_page() -> rx.Component:
    return rx.flex(
        content(),
        background="linear-gradient(ghostwhite, honeydew)",
        flex_direction="column",
        align_items="center",
        min_height="100vh",
    )

def content() -> rx.Component:
    return rx.flex(
        login_tabs(),
        width="100%",
        max_width="1100px",
        padding="24px",
        align="center",
        flex_direction="column",
        flex_basis="auto",
        flex_grow="1",
        flex_shrink="0",
    )

def login_tabs() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.tabs.root(
                rx.center(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            "Login",
                            value="login",
                            on_click=LoginState.set_current_tab("login"),
                        ),
                        rx.tabs.trigger(
                            "Create Account",
                            value="create_account",
                            on_click=LoginState.set_current_tab(
                                "create_account"
                            ),
                        ),
                        size="2",
                    ),
                    width="100%",
                ),
                rx.tabs.content(login_tab(), value="login"),
                rx.tabs.content(create_account_tab(), value="create_account"),
                value=LoginState.current_tab,
                width="100%",
            ),
            justify="center",
        ),
        on_submit=LoginState.event_state_submit_login,
    )


def login_tab() -> rx.Component:
    return rx.flex(
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
            error_login(),
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
                on_click=LoginState.event_state_login_with_sso("google"),
            ),
            rx.image(
                src="/sso/facebook_sso.png",
                height="44px",
                cursor="pointer",
                on_click=LoginState.event_state_login_with_sso("facebook"),
            ),
            rx.image(
                src="/sso/linkedin_sso.png",
                height="44px",
                cursor="pointer",
                on_click=LoginState.event_state_login_with_sso("linkedin_oidc"),
            ),
            width="100%",
            justify="center",
            gap="48px",
            padding="12px 0 12px 0",
        ),
        width="100%",
        gap="24px",
        flex_direction="column",
    )

def error_login() -> rx.Component:
    return rx.cond(
        LoginState.error_message_login,
        rx.callout(
            LoginState.error_message_login,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            margin="20px 0 0 0",
        ),
    )

def create_account_tab() -> rx.Component:
    return rx.flex(
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
            error_create_account(),
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
        width="100%",
        gap="24px",
        flex_direction="column",
    )

def error_create_account() -> rx.Component:
    return rx.cond(
        LoginState.error_message_create_account,
        rx.callout(
            LoginState.error_message_create_account,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            margin="20px 0 0 0",
        ),
    )
