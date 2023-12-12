
from ..auth.auth import AuthState
from ..components.custom import spacer
from ..pages.forbidden import Forbidden

import functools
import reflex as rx

def protected_page(protected_page) -> rx.Component:
    @functools.wraps(protected_page)
    def _wrapper() -> rx.Component:
        return rx.cond(
            rx.State.is_hydrated,
            # If state hydrated, then check if valid token before returning page.
            rx.cond(
                AuthState.token_is_valid,
                protected_page(),
                Forbidden.page(),
            ),
            # If state not hydrated, show loader.
            rx.vstack(
                spacer(height='48px'),
                rx.circular_progress(is_indeterminate=True),
            ),
        )
    return _wrapper