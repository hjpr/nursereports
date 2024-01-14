
from ..auth.auth import AuthState
from loguru import logger
from typing import Iterable

import reflex as rx

def spacer(**props) -> rx.Component:
    """Provide spacer height as int or str. Will be processed as px. Default
    background is white.
    """
    return rx.Box(**props)