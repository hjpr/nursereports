
import functools
import reflex as rx

def spacer(**props) -> rx.Component:
    """Provide spacer height as int or str. Will be processed as px. Default
    background is white.
    """
    return rx.Box(**props)

def loading(page: rx.Component) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond(
            rx.State.is_hydrated,
            page(), # Hydrated show page
            rx.spinner() # Not hydrated, show spinner
        )
    return _wrapper