

from ..components.custom import spacer

import reflex as rx

class Forbidden():
    """403 Error page."""

    route: str = "/error/403"

    def page() -> rx.Component:
        return rx.center(
            rx.vstack(
                spacer(height='48px'),
                rx.circular_progress(
                    is_indeterminate=True,
                    on_mount=rx.redirect('/'),
                ),
            ),
        )