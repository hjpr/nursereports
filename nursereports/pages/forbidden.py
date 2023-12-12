
from ..components.custom import spacer
from reflex.event import EventSpec
from typing import Iterable

import reflex as rx

class ForbiddenState(rx.State):

    def redirect(self) -> Iterable[EventSpec]:
        from ..components.navbar import NavbarState
        yield rx.redirect('/')
        yield NavbarState.set_error_sign_in_message('Sign in to access page.')
        yield NavbarState.set_show_error_sign_in(True)
        yield NavbarState.set_show_sign_in(True)

class Forbidden:
    """403 Error page."""
    route: str = "/error/403"

    def page() -> rx.Component:
        return rx.center(
            rx.vstack(
                spacer(height='48px'),
                rx.circular_progress(
                    is_indeterminate=True,
                    on_mount=ForbiddenState.redirect,
                ),
            ),
        )