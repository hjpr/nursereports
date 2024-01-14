
from loguru import logger

import reflex as rx
import rich

"""
Can grab any custom events (for instance auth_flow) using the State name
in combination with function name...
event_name = state.auth_state.auth_flow
"""

class AuthMiddleware(rx.Middleware):
    """
    Preprocess -
    event.name = 'state.on_load_internal' occurs when navigation requested
    event.name = 'state.hydrate' contains final values pushed to browser
        including cookies accessed via event.router_data.get('access_token')
    """
    def preprocess(self, app, state, event):
        logger.debug(event.name)