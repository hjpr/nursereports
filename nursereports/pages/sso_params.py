
from ..components.custom import spacer

import reflex as rx

def sso_params_page():
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