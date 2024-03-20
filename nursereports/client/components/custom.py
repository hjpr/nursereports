
from ...states.base_state import BaseState

import functools
import reflex as rx

def spacer(**props) -> rx.Component:
    """Provide spacer height as int or str. Will be processed as px. Default
    background is white.
    """
    return rx.box(**props)

def login_protected(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond(
            BaseState.user_is_authenticated,
            page(),
            rx.box()
        )
    return _wrapper

def report_protected(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond(
            BaseState.user_has_reported,
            page(),
            rx.box()
        )
    return _wrapper
