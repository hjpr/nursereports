
from ..components.custom import spacer

import reflex as rx

def sso_page():
    """
    A pseudo endpoint for SSO redirects that runs the auth_handler when hit
    to extract JWT token for access, and refresh token for...well...refreshing.
    """ 
    return rx.center(
        rx.vstack(
            rx.heading(
                "Redirecting after SSO login..."
            ),
            spacer(height='8px'),
            rx.chakra.spinner()
        ),
        height='20em',
    )