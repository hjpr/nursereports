
from ..auth.auth import AuthState
from ..state.base import State

import functools
import reflex as rx

def protected_page(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond(
            State.is_hydrated,
            # If state hydrated, then check if valid token before returning page.
            rx.cond(
                AuthState.token_is_valid,
                page(),
                rx.box(),
            ),
            # If state not hydrated, show loader.
            rx.center(
                rx.circular_progress(is_indeterminate=True)
            )
        )
    return _wrapper