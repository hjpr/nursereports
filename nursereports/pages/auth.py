
from ..components.custom import spacer

import reflex as rx

def auth():
    """
    A pseudo endpoint for SSO redirects that runs the auth_handler when hit
    to extract JWT token for access, and refresh token for...well...refreshing.
    """ 
    return rx.center(
        rx.vstack(
            rx.heading(
                "Processing login, redirecting...",
                size='md',
            ),
            spacer(height='8px'),
            rx.circular_progress(
                is_indeterminate=True,
            ),
        ),
        height='20em',
    )

def deauth():
    """
    A pseudo endpoint for SSO redirects that runs the deauth_handler when hit
    to remove user information per request of user.
    """
    return rx.center(
        rx.vstack(
            rx.heading(
                "Removing user info, redirecting...",
                size='md',
            ),
            spacer(height='8px'),
            rx.circular_progress(
                is_indeterminate=True,
            ),
        ),
        height='20em',
    )