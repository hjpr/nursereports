from ..server.supabase import supabase_get_new_access_token

from loguru import logger
from typing import Callable, Iterable

import reflex as rx


class AuthState(rx.State):
    access_token: str = rx.Cookie(
        name="access_token",
        same_site="strict",
        secure=True,
    )
    refresh_token: str = rx.Cookie(
        name="refresh_token",
        same_site="strict",
        secure=True,
    )

    def refresh_access_token(self) -> Iterable[Callable]:
        """
        Refresh JWT token using refresh token.
        """
        try:
            access_token = self.access_token
            refresh_token = self.refresh_token
            tokens = supabase_get_new_access_token(access_token, refresh_token)
            self.access_token = tokens.get("access_token", "")
            self.refresh_token = tokens.get("refresh_token", "")
        except Exception as e:
            logger.critical(e)
            yield rx.toast.error("Unable to refresh credentials.")

    def event_state_logout(self) -> Iterable[Callable]:
        """
        Send to root and reset all state vars.
        """
        yield rx.redirect("/")
        yield self.reset()
        yield rx.toast.success("Logged out.")
