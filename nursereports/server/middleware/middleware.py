
from loguru import logger

import reflex as rx

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
        # if event.name == "state.on_load_internal":
        #     rich.inspect(event)
        # if event.name == "state.set_is_hydrated":
        #     rich.inspect(state.substates['report_state'])
        # if not event.name == "state.on_load_internal" or\
        #     not event.name == "state.update_vars_internal" or\
        #     not event.name == "state.set_is_hydrated":
        #     logger.debug(f"{state.router.session.client_token} - {event.name}")
        pass