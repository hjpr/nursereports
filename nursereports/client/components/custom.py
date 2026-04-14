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
        return rx.cond(UserState.user_is_logged_in, page(), rx.box("This resource is protected. Please login to access."))

    return _wrapper

def report_protected(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond((UserState.user_is_logged_in & ~UserState.user_needs_onboarding), page(), rx.box("This resource is protected. Requires submitting a report to access."))

    return _wrapper
