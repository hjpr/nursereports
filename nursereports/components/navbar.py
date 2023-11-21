
from ..auth.auth import AuthState
from ..components.custom import spacer
from ..state.base import State

import reflex as rx
import rich

class NavbarState(State):

    # Show if True.
    show_alert: bool = False
    show_c2a: bool = True
    show_feedback: bool = False
    show_sign_in: bool = False

    # Alert modal message.
    alert_message: str = None

    # Show error under buttons during sign in/up and providing feedback.
    show_error_sign_in: bool = False
    show_error_create_account: bool = False
    show_error_feedback: bool = False

    # Content of errors during sign in/up and providing feedback.
    error_sign_in_message: str = None
    error_create_account_message: str = None
    error_feedback_message: str = None

    # Tracks if user is signed in. Client-side value. Untrusted but helps
    # to set some conditional items as visible.
    is_authenticated: bool = False

    # Login loading status...
    sign_in_working: bool = False
    create_account_working: bool = False
    submit_feedback_working: bool = False

    # Show/hide configurable alert modal.
    def toggle_alert(self):
        self.show_alert = not self.show_alert

    # Show/close c2a
    def toggle_c2a(self):
        self.show_c2a = not self.show_c2a

    # Show/close feedback modal.
    def toggle_feedback(self):
        self.show_feedback = not self.show_feedback

    # Show/close login modal.
    def toggle_login(self):
        self.show_sign_in = not self.show_sign_in
        self.show_error_sign_in = False
        self.show_error_create_account = False
        self.error_sign_in_message = None
        self.error_create_account_message = None

def navbar() -> rx.Component:
    """
    Main navbar for site. Contains the components and states for menus and
    navigation. Authorization logic and components are utilized by navbar but
    are contained in auth.py.
    """
    return rx.box(

        # MODAL FOR ALERTS
        alert_modal(),

        # MODAL FOR C2A FEEDBACK
        feedback_modal(),

        # MODAL FOR SIGN IN
        login_modal(),

        # NAVBAR CONTAINER
        rx.center(

            # SITE HEADING
            rx.image(
                 src='/vector/icon_web_header.svg',
                 height='32px',
                 width='32px',
                 margin_left='12px',
                 margin_right='4px',
            ),

            rx.heading(
                "Nurse Reports",
                display=['none', 'none', 'inline', 'inline', 'inline'],
                margin_left='8px',
                margin_right='8px',
                size='lg',
            ),
            rx.badge(
                "Beta",
                color_scheme='teal',
                display='inline',
                margin_right= '20px',
                margin_left='4px',
            ),

            cond_options(),

            rx.spacer(),

            cond_account(),

            # STYLING FOR NAVBAR
            height='60px',
            padding_x='24px',
            padding_y='12px',
            width='100%',
        ),

        c2a(),

        # STYLING FOR NAVBAR CONTAINER
        backdropFilter='blur(8px)',
        bg='rgba(255, 255, 255, 0.9)',
        border_bottom='1px solid lightgrey',
        position='fixed',
        top='0px',
        flex_direction='down',
        width='100%',
        z_index='5',
    )

def cond_account() -> rx.Component:
    """
    Conditional sign in/account button. Shows a clickable button 'Sign in'
    that toggles the login modal using 'login_modal' when not logged in.
    When logged in shows an avatar that opens menu on click.
    """
    return rx.cond(
        NavbarState.is_authenticated,

        # ACCOUNT OPTIONS IF LOGGED IN
        rx.menu(
            rx.menu_button(
                rx.avatar(
                    size='xs',
                ),
            ),
            rx.menu_list(
                rx.menu_item("Account"),
                rx.menu_item("Sign Out"),
            ),
        ),

        # SIGN IN IF NOT LOGGED IN
        rx.button(
            "Sign In",
            variant='ghost',
            size='sm',
            on_click=NavbarState.toggle_login()
        ),
    )

def cond_options() -> rx.Component:
            return rx.cond(
                NavbarState.is_authenticated,
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
                    ),
                ),
            )

def alert_modal() -> rx.Component:
    """
    Alert modal rendered when we want to show user a message. Uses 'show_alert'
    as the bool which controls if it is in view or not. Message contained in
    alert_message.
    """
    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(

                    # MODAL HEADER
                    rx.modal_header(
                        "Message"
                    ),
                    rx.modal_body(
                        NavbarState.alert_message
                    ),
                    rx.modal_footer(
                        rx.button(
                            "Close",
                            on_click=NavbarState.toggle_alert,
                        ),
                    ),
                    # STYLING FOR MODAL CONTENT
                    top='-5px',
                ),
                # STYLING FOR MODAL OVERLAY
                backdrop_filter='blur(2px)',
            ),
            # STYLING FOR MODAL
            motion_preset='scale',
            is_open=NavbarState.show_alert,
            on_overlay_click=NavbarState.toggle_alert()
        ),
    )

def feedback_modal() -> rx.Component:
    """"
    Feedback modal rendered when user clicks c2a to submit site issue. Uses
    'show_feedback' as bool which controls if displayed or not.
    """
    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    
                    # WRAP HEADER - BODY - FOOTER AS FORM
                    rx.form(

                        # MODAL HEADER
                        rx.modal_header(
                            rx.hstack(
                                rx.text("Submit issues/feedback..."),
                                rx.spacer(),
                                rx.button(                        
                                    rx.icon(
                                        tag='close',
                                    ),
                                    size='sm',
                                    variant='ghost',
                                    _hover='none',
                                    on_click=NavbarState.toggle_feedback,
                                ),
                                width='100%',
                            ),
                        ),

                        # MODAL BODY
                        rx.modal_body(
                            rx.text_area(
                                placeholder='Enter here...',
                                height='100%',
                                is_disabled=~NavbarState.is_authenticated,
                                is_required=True,
                            ),
                            height='10em',
                        ),

                        # MODAL FOOTER
                        rx.modal_footer(
                            rx.cond(
                                ~NavbarState.is_authenticated,
                                rx.alert(
                                    rx.alert_icon(),
                                    rx.alert_title(
                                        "To help combat spam, please login."
                                    ),
                                status="error",
                                border_radius='6px',
                                ),
                                rx.button(
                                    "Submit",
                                    width='100%',
                                    type_='submit',
                                    variant='solid',
                                    color_scheme='teal',
                            ),

                            ),
                            flex_direction='column',
                        ),

                    ),

                    # STYLING FOR MODAL CONTENT
                    top='-5px',
                ),
                # STYLING FOR MODAL OVERLAY
                backdrop_filter='blur(2px)',
            ),
            # STYLING FOR MODAL COMPONENT

            is_open=NavbarState.show_feedback,
            on_overlay_click=NavbarState.toggle_feedback,
        ),
    )

def login_modal() -> rx.Component:
    """
    Login modal rendered when user clicks 'sign in'. Uses 'show_sign_in'
    as the bool which controls if displayed or not.
    """
    return rx.box(
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(

                    # MODAL HEADER
                    rx.modal_header(
                        rx.hstack(
                            rx.spacer(),
                            rx.button(                        
                                rx.icon(
                                    tag='close',
                                ),
                                size='sm',
                                variant='ghost',
                                _hover='none',
                                on_click=NavbarState.toggle_login(),
                            ),
                            width='100%',
                        ),
                    ),

                    # MODAL BODY
                    rx.modal_body(
                        rx.tabs(
                            rx.tab_list(
                                rx.tab("Sign in"),
                                rx.tab("Create account"),
                            ),
                            rx.tab_panels(
                                rx.tab_panel(
                                    
                                    # TAB PANEL SIGN IN
                                    rx.form(
                                        rx.vstack(
                                            spacer(height='28px'),
                                            rx.input(
                                                placeholder='E-Mail',
                                                id='sign_in_email',
                                                is_required=True,
                                            ),
                                            spacer(height='8px'),
                                            rx.input(
                                                placeholder='Password',
                                                id='sign_in_password',
                                                type_='password',
                                                is_required=True,
                                            ),
                                            spacer(height='8px'),
                                            rx.button(
                                                'Sign in',
                                                variant='solid',
                                                color_scheme='teal',
                                                width='100%',
                                                type_='submit',
                                                is_loading=NavbarState.sign_in_working,
                                            ),
                                            rx.cond(
                                                NavbarState.show_error_sign_in,
                                                rx.alert(
                                                    rx.alert_icon(),
                                                    rx.alert_title(
                                                        NavbarState.error_sign_in_message
                                                    ),
                                                    status="error",
                                                    border_radius='6px',
                                                ),
                                            ),
                                            width='100%',
                                        ),
                                        on_submit=AuthState.email_sign_in,
                                    ),

                                ),
                                rx.tab_panel(

                                    # TAB PANEL CREATE ACCOUNT
                                    rx.form(
                                        rx.vstack(
                                            spacer(height='28px'),
                                            rx.input(
                                                placeholder='E-Mail',
                                                id='create_account_email',
                                                is_required=True,
                                            ),
                                            spacer(height='8px'),
                                            rx.input(
                                                placeholder='Password',
                                                id='create_account_password',
                                                type_='password',
                                                is_required=True,
                                            ),
                                            rx.input(
                                                placeholder='Confirm Password',
                                                id='create_account_password_confirm',
                                                type_='password',
                                                is_required=True,
                                            ), 
                                            spacer(height='8px'),                                     
                                            rx.button(
                                                'Create account',
                                                color_scheme='teal',
                                                variant='solid',
                                                width='100%',
                                                type_='submit',
                                                is_loading=NavbarState.create_account_working,
                                            ),
                                            rx.cond(
                                                NavbarState.show_error_create_account,
                                                rx.alert(
                                                    rx.alert_icon(),
                                                    rx.alert_title(
                                                        NavbarState.error_create_account_message,
                                                    ),
                                                    status="error",
                                                    border_radius='6px',
                                                ),
                                            ),
                                            width='100%',
                                        ),
                                        on_submit=AuthState.email_create_account
                                    ),

                                ),
                            ),
                            align='center',
                            is_fitted=True,
                            variant='enclosed',
                        ),
                    ),

                    # MODAL FOOTER - SINGLE SIGN ON
                    rx.modal_footer(
                        rx.vstack(
                            rx.hstack(
                                rx.divider(),
                                rx.text(
                                    "Or continue with",
                                    width='100%',
                                    margin_x='16px',
                                    text_align='center',
                                    ),
                                rx.divider(),
                                width='100%',
                            ),
                            spacer(height='24px'),
                            rx.hstack(
                                rx.spacer(),
                                rx.image(
                                    src='/sso/google_sso.png',
                                    height='44px',
                                    cursor='pointer',
                                    on_click=AuthState.sso_sign_in('google'),
                                ),
                                rx.spacer(),
                                rx.image(
                                    src='/sso/facebook_sso.png',
                                    height='44px',
                                    cursor='pointer',
                                    on_click=AuthState.sso_sign_in('facebook')
                                ),
                                rx.spacer(),
                                rx.image(
                                    src='/sso/linkedin_sso.png',
                                    height='44px',
                                    cursor='pointer',
                                    on_click=AuthState.sso_sign_in('linkedin_oidc')
                                ),
                                rx.spacer(),
                                width='100%',
                                padding_x='40px',
                            ),
                            spacer(height='32px'),
                            width='100%',
                        ),
                    ),
                    # STYLING FOR MODAL CONTENT
                    top='-5px',
                ),
                # STYLING FOR MODAL OVERLAY
                backdrop_filter='blur(2px)',
            ),
            # STYLING FOR MODAL COMPONENT
            motion_preset='scale',
            is_open=NavbarState.show_sign_in,
            on_overlay_click=NavbarState.toggle_login()
        ),
    )

def c2a() -> rx.Component:
    """
    Conditional call to action below navbar. Shows on first visit to site
    and can be closed by user with the 'close' button.
    """
    return rx.cond(
        NavbarState.show_c2a,
        rx.hstack(
            rx.center(
                rx.button(
                    "In Beta. Click here to submit site issue.",
                    size='sm',
                    variant='ghost',
                    color='white',
                    _hover='none',
                    on_click=NavbarState.toggle_feedback,
                ),
                width='100%',
            ),
            rx.button(
                rx.icon(
                    tag='close',
                    color='white',
                ),
                size='sm',
                variant='ghost',
                _hover='none',
                on_click=NavbarState.toggle_c2a,
            ),

            # STYLING FOR C2A CONTAINER
            bg='rgba(0, 128, 128, 0.8)', # teal
            box_shadow='inset 0px 4px 5px -5px rgba(0, 0, 0, 0.5)',
            height='40px',
            padding_x='12px',
            padding_y='4px',
        ),
    )

def c2a_spacer() -> rx.Component:
    """
    Sets spacer to allow elements to move when c2a is closed.
    """
    return rx.cond(
        NavbarState.show_c2a,
        rx.box(
            height='100px',
            width='100%',
        ),
        rx.box(
            height='60px',
            width='100%',
        ),
    )