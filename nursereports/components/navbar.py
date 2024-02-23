
from ..components.custom import spacer
from ..states.auth import AuthState
from ..states.navbar import NavbarState

import reflex as rx

def navbar() -> rx.Component:
    """
    Main navbar component.
    """
    return rx.box(

        # MODAL FOR ALERTS
        alert_modal(),

        # MODAL FOR C2A FEEDBACK
        feedback_modal(),

        # MODAL FOR SIGN IN
        # login_modal(),

        # NAVBAR CONTAINER
        rx.center(

            # SITE HEADING
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

            # STYLING FOR NAVBAR
            height='60px',
            padding_x='24px',
            padding_y='12px',
            width='100%',
        ),

        # STYLING FOR NAVBAR CONTAINER
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
    """
    Conditional sign in/account button. Shows a clickable button 'Sign in'
    that toggles the login modal using 'login_modal' when not logged in.
    When logged in shows an avatar that opens menu on click.
    """
    return rx.cond(
        AuthState.user_is_authenticated,
        # ACCOUNT OPTIONS IF LOGGED IN
        rx.menu.root(
            rx.menu.trigger(
                rx.avatar()
            ),
            rx.menu.content(
                rx.menu.item("Account"),
                rx.menu.item("Logout", on_click=AuthState.logout)
            )
        ),
        # SIGN IN IF NOT LOGGED IN
        rx.button(
            "Sign In",
            on_click=NavbarState.toggle_login,
        ),
    )

def cond_options() -> rx.Component:
    """
    Links that populate next to header once logged in and user has
    submitted a report.
    """
    return rx.cond(
        AuthState.user_is_authenticated & AuthState.user_has_reported,
        # MENU OPTIONS IF LOGGED IN
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
    """
    Renders alert modal if NavbarState.alert_message contains a str.
    """
    return rx.cond(
        NavbarState.alert_message,
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title(
                    "Site message."
                ),
                rx.alert_dialog.description(NavbarState.alert_message),
                rx.alert_dialog.action("OK", on_click=NavbarState.set_alert_message(""))
            ),
            backdrop_filter='blur(2px)'
        )
    )

def feedback_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Provide feedback."),
            rx.dialog.description(
                rx.text_area(
                    placeholder="What can we improve?"
                )
            ),
            spacer(height='16px'),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant='soft',
                        on_click=NavbarState.toggle_feedback
                    )
                ),
                rx.dialog.close(
                    rx.button(
                        "Submit",
                        on_click=NavbarState.toggle_feedback
                    )
                ),
                spacing='3',
                justify='end'
            )
        ),
        open=NavbarState.show_feedback
    )

# def login_modal() -> rx.Component:
#     """
#     Renders login modal if NavbarState.show_sign_in is True.
#     """
#     return rx.box(
#         rx.modal(
#             rx.modal_overlay(
#                 rx.modal_content(
#                     # MODAL HEADER
#                     rx.modal_header(
#                         rx.hstack(
#                             rx.spacer(),
#                             rx.button(                        
#                                 rx.icon(
#                                     tag='close'
#                                 ),
#                                 size='sm',
#                                 variant='ghost',
#                                 _hover='none',
#                                 on_click=NavbarState.toggle_login()
#                             ),
#                             width='100%',
#                         )
#                     ),
#                     # MODAL BODY
#                     rx.modal_body(
#                         rx.tabs(
#                             rx.tab_list(
#                                 rx.tab(
#                                     "Sign in",
#                                     font_weight='700',
#                                     ),
#                                 rx.tab(
#                                     "Create account",
#                                     font_weight='700',
#                                     ),
#                             ),
#                             rx.tab_panels(
#                                 rx.tab_panel(
#                                     # TAB PANEL SIGN IN
#                                     rx.form(
#                                         rx.vstack(
#                                             spacer(height='28px'),
#                                             rx.text(
#                                                 "Email",
#                                                 text_align='left',
#                                                 font_size='0.9em',
#                                                 width='100%',
#                                                 ),
#                                             rx.input(
#                                                 placeholder='Enter e-mail',
#                                                 id='sign_in_email',
#                                                 is_required=True,
#                                             ),
#                                             spacer(height='8px'),
#                                             rx.text(
#                                                 "Password",
#                                                 text_align='left',
#                                                 font_size='0.9em',
#                                                 width='100%',
#                                                 ),
#                                             rx.input(
#                                                 placeholder='Enter password',
#                                                 id='sign_in_password',
#                                                 type_='password',
#                                                 is_required=True,
#                                             ),
#                                             spacer(height='8px'),
#                                             rx.button(
#                                                 'Sign in',
#                                                 variant='solid',
#                                                 color_scheme='teal',
#                                                 width='100%',
#                                                 type_='submit',
#                                                 is_loading=~rx.State.is_hydrated
#                                             ),
#                                             rx.cond(
#                                                 NavbarState.error_sign_in_message,
#                                                 rx.alert(
#                                                     rx.alert_icon(),
#                                                     rx.alert_title(
#                                                         NavbarState.error_sign_in_message
#                                                     ),
#                                                     status="error",
#                                                     border_radius='6px',
#                                                 )
#                                             ),
#                                             width='100%',
#                                         ),
#                                         on_submit=AuthState.email_sign_in,
#                                     )
#                                 ),
#                                 rx.tab_panel(
#                                     # TAB PANEL CREATE ACCOUNT
#                                     rx.form(
#                                         rx.vstack(
#                                             spacer(height='28px'),
#                                             rx.text(
#                                                 "Email",
#                                                 text_align='left',
#                                                 font_size='0.9em',
#                                                 width='100%',
#                                                 ),                                           
#                                             rx.input(
#                                                 placeholder='Enter e-mail',
#                                                 id='create_account_email',
#                                                 is_required=True,
#                                             ),
#                                             spacer(height='8px'),
#                                             rx.text(
#                                                 "Password",
#                                                 text_align='left',
#                                                 font_size='0.9em',
#                                                 width='100%',
#                                                 ),                                            
#                                             rx.input(
#                                                 placeholder='Enter password',
#                                                 id='create_account_password',
#                                                 type_='password',
#                                                 is_required=True,
#                                             ),
#                                             rx.text(
#                                                 "Confirm password",
#                                                 text_align='left',
#                                                 font_size='0.9em',
#                                                 width='100%',
#                                                 ),                                           
#                                             rx.input(
#                                                 placeholder='Re-enter password',
#                                                 id='create_account_password_confirm',
#                                                 type_='password',
#                                                 is_required=True,
#                                             ), 
#                                             spacer(height='8px'),                                     
#                                             rx.button(
#                                                 'Create account',
#                                                 color_scheme='teal',
#                                                 variant='solid',
#                                                 width='100%',
#                                                 type_='submit',
#                                                 is_loading=~rx.State.is_hydrated,
#                                             ),
#                                             rx.cond(
#                                                 NavbarState.error_create_account_message,
#                                                 rx.alert(
#                                                     rx.alert_icon(),
#                                                     rx.alert_title(
#                                                         NavbarState.error_create_account_message,
#                                                     ),
#                                                     status="error",
#                                                     border_radius='6px'
#                                                 )
#                                             ),
#                                             width='100%'
#                                         ),
#                                         on_submit=AuthState.email_create_account
#                                     )
#                                 )
#                             ),
#                             align='center',
#                             is_fitted=True,
#                             variant='enclosed'
#                         )
#                     ),
#                     # MODAL FOOTER - SINGLE SIGN ON
#                     rx.modal_footer(
#                         rx.vstack(
#                             rx.hstack(
#                                 rx.divider(),
#                                 rx.text(
#                                     "Or continue with",
#                                     width='100%',
#                                     margin_x='16px',
#                                     text_align='center',
#                                     font_size='0.9em',
#                                     ),
#                                 rx.divider(),
#                                 width='100%'
#                             ),
#                             spacer(height='24px'),
#                             rx.hstack(
#                                 rx.spacer(),
#                                 rx.image(
#                                     src='/sso/google_sso.png',
#                                     height='44px',
#                                     cursor='pointer',
#                                     on_click=AuthState.sso_sign_in('google')
#                                 ),
#                                 rx.spacer(),
#                                 rx.image(
#                                     src='/sso/facebook_sso.png',
#                                     height='44px',
#                                     cursor='pointer',
#                                     on_click=AuthState.sso_sign_in('facebook')
#                                 ),
#                                 rx.spacer(),
#                                 rx.image(
#                                     src='/sso/linkedin_sso.png',
#                                     height='44px',
#                                     cursor='pointer',
#                                     on_click=AuthState.sso_sign_in('linkedin_oidc')
#                                 ),
#                                 rx.spacer(),
#                                 width='100%',
#                                 padding_x='40px'
#                             ),
#                             spacer(height='32px'),
#                             width='100%'
#                         ),
#                     ),
#                     # STYLING FOR MODAL CONTENT
#                     top='-5px',
#                 ),
#                 # STYLING FOR MODAL OVERLAY
#                 backdrop_filter='blur(2px)',
#             ),
#             # STYLING FOR MODAL COMPONENT
#             motion_preset='scale',
#             is_open=NavbarState.show_sign_in,
#             on_overlay_click=NavbarState.toggle_login()
#         )
#     )

def c2a_spacer() -> rx.Component:
    """
    Inserts spacer if NavbarState.show_c2a is True, to allow page to
    space correctly if c2a is open or closed.
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