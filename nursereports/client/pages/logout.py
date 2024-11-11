from .loading import loading_page
from ...states import BaseState

import reflex as rx


@rx.page(
    route="/logout/[logout_reason]",
    title="Logging out...",
    on_load=BaseState.event_state_logout,
)
def logout_page() -> rx.Component:
    return rx.box(loading_page())
