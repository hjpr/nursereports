
from ..components.custom import spacer

import reflex as rx

def deauth_api():
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