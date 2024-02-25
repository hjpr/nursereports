
from ..components.custom import spacer
from ..events.auth import event_supabase_sso_login
from ..states.base import BaseState
from ..states.navbar import NavbarState

import reflex as rx

def navbar() -> rx.Component:
    return rx.box(
        alert_modal(),
        feedback_modal(),
        login_modal(),
        rx.center(
            rx.image(
                 src='/vector/icon_web_header.svg',
                 height='32px',
                 width='32px',
                 margin_left='12px',
                 margin_right='4px',
                 cursor='pointer',
                 on_click=rx.redirect("/")
            ),
            rx.heading(
                "Nurse Reports",
                size='6',
                display=['none', 'none', 'inline', 'inline', 'inline'],
                margin_left='8px',
                margin_right='8px',
                cursor='pointer',
                on_click=rx.redirect('/'),
            ),
            rx.badge(
                "Beta",
                display='inline',
                margin_right= '20px',
                margin_left='4px',
            ),
            cond_options(),
            rx.spacer(),
            cond_account(),
            height='60px',
            padding_x='24px',
            padding_y='12px',
            width='100%',
        ),
        backdropFilter='blur(8px)',
        bg='rgba(255, 255, 255, 0.9)',
        position='sticky',
        top='0px',
        box_shadow='0px 4px 5px -5px rgba(0, 0, 0, 0.5)',
        flex_direction='down',
        width='100%',
        z_index='5',
    )

def cond_account() -> rx.Component:
    return rx.cond(
        BaseState.user_is_authenticated,
        rx.menu.root(
            rx.menu.trigger(
                rx.avatar()
            ),
            rx.menu.content(
                rx.menu.item("Account"),
                rx.menu.item("Logout", on_click=NavbarState.event_state_logout)
            )
        ),
        rx.button(
            "Sign In",
            on_click=NavbarState.event_ui_toggle_login,
        ),
    )

def cond_options() -> rx.Component:
    return rx.cond(
        BaseState.user_is_authenticated & BaseState.user_has_reported,
        rx.hstack(
            rx.link(
                "Hospital Search",
                display=['none', 'inline', 'inline', 'inline', 'inline'],
                padding_x='12px',
            ),
            rx.link(
                "State Overview",
                display=['none', 'inline', 'inline', 'inline', 'inline'],
                padding_x='12px'
            )
        )
    )

def alert_modal() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title(
                "Site message."
            ),
            rx.alert_dialog.description(NavbarState.alert_message),
            rx.alert_dialog.action("OK", on_click=NavbarState.set_alert_message(""))
        ),
        open=NavbarState.show_alert_message
    )

def feedback_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Provide feedback."),
            rx.form(
                rx.dialog.description(
                    rx.text_area(
                        name='feedback',
                        placeholder="What can we improve?",
                        height='100px',
                        max_length=500,
                        spell_check=True
                    )
                ),
                spacer(height='16px'),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            type='button',
                            variant='soft',
                            on_click=NavbarState.event_ui_toggle_feedback,
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Submit",
                            type='submit',
                        )
                    ),
                    spacing='3',
                    justify='end',
                ),
                spacer(height='4px'),
                rx.cond(
                    NavbarState.error_feedback_message,
                    rx.callout(
                        NavbarState.error_feedback_message,
                        icon="alert_triangle",
                        color_scheme="red",
                        role="alert"
                    )
                ),
                on_submit=NavbarState.event_state_submit_feedback
            )
        ),
        open=NavbarState.show_feedback,
    )

def login_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.flex(
                    rx.button(
                        rx.icon(
                            tag='x'
                        ),
                        size='1',
                        variant='ghost',
                        on_click=NavbarState.set_show_login(False)
                    ),
                    justify='end',
                    width='100%'
                )
            ),
            rx.form(
                rx.flex(
                    rx.tabs.root(
                        rx.center(
                            rx.tabs.list(
                                rx.tabs.trigger(
                                    "Login",
                                    value='login',
                                    on_click=NavbarState.set_login_tab(
                                        "login"
                                    )
                                ),
                                rx.tabs.trigger(
                                    "Create Account",
                                    value='create_account',
                                    on_click=NavbarState.set_login_tab(
                                        "create_account"
                                    )
                                ),
                                size='2',
                            ),
                            width='100%'
                        ),
                        rx.tabs.content(
                            login_tab_login(),
                            value="login",
                        ),
                        rx.tabs.content(
                            login_tab_account(),
                            value='create_account'
                        ),
                        value=NavbarState.login_tab,
                        width='100%',
                    ),
                    justify='center',
                ),
                on_submit=NavbarState.event_state_login_modal_submit
            ),
            max_width='400px',
            on_escape_key_down=NavbarState.set_show_login(False),
        ),
        open=NavbarState.show_login,
    )

def login_tab_login() -> rx.Component:
    return rx.flex(
        spacer(),
        rx.heading(
            "Login to your account",
            size='6',
            text_align='center',
            width='100%'
        ),
        rx.center(
            rx.vstack(
                rx.text(
                    "Email",
                    size='2'
                ),
                rx.input(
                    placeholder='Enter email',
                    name='login_email',
                    size='3',
                    required=True,
                )
            )
        ),
        rx.center(
            rx.vstack(
                rx.text(
                    "Password",
                    size='2'
                    ),
                rx.input(
                    placeholder='Enter password',
                    name='login_password',
                    type='password',
                    size='3',
                    required=True
                )
            )
        ),
        rx.center(
            rx.button(
                "Login",
                width='100%',
                type='submit'
            ),
            margin_top="12px",
            width='100%'
        ),
        rx.cond(
            NavbarState.error_sign_in_message,
            rx.callout(
                NavbarState.error_sign_in_message,
                icon="alert_triangle",
                color_scheme="red",
                role="alert"
            )
        ),
        rx.hstack(
            rx.divider(),
            rx.text(
                "OR",
                size='2',
                padding='6px',
                white_space='nowrap'
                ),
            rx.divider(),
            align='center',
            width='100%'
        ),
        rx.hstack(
            rx.image(
                src='/sso/google_sso.png',
                height='44px',
                cursor='pointer',
                on_click=event_supabase_sso_login('google')
            ),
            rx.image(
                src='/sso/facebook_sso.png',
                height='44px',
                cursor='pointer',
                on_click=event_supabase_sso_login('facebook')
            ),
            rx.image(
                src='/sso/linkedin_sso.png',
                height='44px',
                cursor='pointer',
                on_click=event_supabase_sso_login('linkedin_oidc')
            ),
            width='100%',
            justify='center',
            gap='48px'
        ),
        spacer(),
        width='100%',
        gap='24px',
        flex_direction='column'
    )

def login_tab_account() -> rx.Component:
    return rx.flex(
        spacer(),
        rx.heading(
            "Create new account",
            size='6',
            text_align='center',
            width='100%'
        ),
        rx.center(
            rx.vstack(
                rx.text(
                    "Email",
                    size='2'
                ),
                rx.input(
                    placeholder='Enter email',
                    name='create_account_email',
                    size='3',
                    required=True,
                )
            )
        ),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.text(
                        "Password",
                        size='2'
                    ),
                    rx.input(
                        placeholder="Enter password",
                        name='create_account_password',
                        type='password',
                        size='3',
                        required=True
                    )
                ),
                rx.vstack(
                    rx.text(
                        "Confirm password",
                        size='2'
                    ),
                    rx.input(
                        placeholder="Re-enter password",
                        name='create_account_password_confirm',
                        type='password',
                        size='3',
                        required=True
                    )
                )
            )
        ),
        rx.center(
            rx.switch(
                name='create_account_student',
                default_checked=False,
            ),
            rx.text(
                "I'm a ",
                rx.popover.root(
                    rx.popover.trigger(
                        rx.link(
                            "nursing student.",
                            color_scheme='blue',
                            size='2'
                        ),
                    ),
                    rx.popover.content(
                        rx.text(
                            """Students can access our resources
                            for 1 year and then must submit a report
                            after hire to maintain access."""
                        )
                    )
                ),
                size='2'
            ),
            gap='8px',
            margin_top='8px'
        ),
        rx.center(
            rx.button(
                "Create account",
                width='100%',
                type='submit'
            ),
            margin_top='12px',
            width='100%'
        ),
        rx.cond(
            NavbarState.error_create_account_message,
            rx.callout(
                NavbarState.error_create_account_message,
                icon='alert_triangle',
                color_scheme='red',
                role='alert'
            )
        ),
        rx.center(
            rx.hstack(
                rx.link(
                    "Privacy Policy",
                    size='2'
                ),
                rx.divider(width='12px'),
                rx.link(
                    "AI Policy",
                    size='2'
                ),
                align='center'
            )
        ),
        spacer(),
        width='100%',
        gap='24px',
        flex_direction='column'
    )