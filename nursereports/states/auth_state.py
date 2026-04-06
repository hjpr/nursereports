from suplex import Suplex

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class AuthState(Suplex):

    def refresh_access_token(self) -> Callable | None:
        """
        Refresh JWT token using refresh token.
        """
        try:
            self.refresh_session()
            return None
        except Exception as e:
            logger.critical(e)
            return rx.toast.error("Unable to refresh credentials.")

    def event_state_logout(self) -> Iterable[Callable]:
        """
        Send to root and reset all state vars.
        """
        try:
            self.log_out()
        except Exception:
            pass
        yield rx.redirect("/")
        yield self.reset()
        return rx.toast.success("Logged out.")
