from ...states import UserState

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
        return rx.cond(UserState.user_claims_authenticated, page(), rx.box("401 Placeholder"))

    return _wrapper

def report_protected(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond((UserState.user_claims_authenticated & ~UserState.user_needs_onboarding), page(), rx.box("401 Placeholder"))

    return _wrapper
