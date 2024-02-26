
from functools import wraps
from ...states.base import BaseState

import reflex as rx

def spacer(**props) -> rx.Component:
    """Provide spacer height as int or str. Will be processed as px. Default
    background is white.
    """
    return rx.box(**props)

def protected(page: rx.Component) -> rx.Component:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> rx.Component:
            if BaseState.user_is_authenticated:
                return func(*args, **kwargs)
            else:
                return rx.chakra.spinner()
        return wrapper
    return decorator