
from .loading import loading_page
from ...states.navbar import NavbarState

import reflex as rx

@rx.page(
    route='/logout',
    title='Logging out...',
    on_load=NavbarState.event_state_logout
)
def logout_page() -> rx.Component:
    return rx.box(
        loading_page()
    )