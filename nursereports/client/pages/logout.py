from .loading import loading_page
from ...states import AuthState

import reflex as rx


@rx.page(
    route="/logout/[logout_reason]",
    title="Logging out...",
    on_load=AuthState.logout,
)
def logout_page() -> rx.Component:
    return rx.box(loading_page())
