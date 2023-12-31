
from ..components.custom import spacer

import reflex as rx

class AuthAPI:

    route: str = '/api/v1/auth'

    def page():
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