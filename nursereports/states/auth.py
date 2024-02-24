
from ..states.base import BaseState
from ..states.navbar import NavbarState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx

class AuthState(BaseState):

    @rx.var
    def auth_params(self):
        """
        Pulls params from /api/auth/[params]
        """
        return self.router.page.params.get('params')
        
    def parse_auth(self) -> Iterable[Callable]:
        """
        Pull params from url and redirects to dashboard.
        """
        if self.auth_params:
            try:
                fragment = self.auth_params.split("#")[1]
                access_token = fragment.split("&")[0].split("=")[1]
                refresh_token = fragment.split("&")[4].split("=")[1]
            except Exception as e:
                logger.critical(f"Unable to parse url - {e}")
                yield rx.redirect("/")
                yield NavbarState.set_alert_message("Invalid login information during SSO attempt.")
            self.access_token = access_token
            self.refresh_token = refresh_token
            yield rx.redirect("/dashboard")
        else:
            logger.warning("No auth parameters found.")
            yield rx.redirect("/")
            yield NavbarState.set_alert_message("Empty SSO information.")