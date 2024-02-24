
from loguru import logger

import reflex as rx
import rich

"""
Can grab any custom events (for instance auth_flow) using the State name
in combination with function name...
event_name = state.auth_state.auth_flow
"""

class LoggingMiddleware(rx.Middleware):
    """
    Preprocess -
    event.name = 'state.on_load_internal' occurs when navigation requested
    event.name = 'state.hydrate' contains final values pushed to browser
        including cookies accessed via event.router_data.get('access_token')
    """
    def preprocess(self, app, state, event):
        logger.debug(f"{state.router.session.session_id} - {event.name}")
        # if event.name == "state.on_load_internal":
        #     rich.inspect(event)
        # if event.name == "state.set_is_hydrated":
        #     rich.inspect(state.substates['report_state'])