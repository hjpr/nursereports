
from ..events.auth import event_supabase_sso_login
from ..states.base import BaseState
from ..states.navbar import NavbarState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx

class AuthState(BaseState):
    @rx.var
    def auth_params(self):
        return self.router.page.params.get('provider')
    
    def event_state_sso_onload(self) -> Callable:
        redirect = event_supabase_sso_login(self.auth_params)
        return redirect
        
    def event_state_sso_parse_params(self) -> Iterable[Callable]:
        if self.auth_params[2] == "#":
            fragment = self.auth_params.split("#")[1]
            access_token = fragment.split("&")[0].split("=")[1]
            refresh_token = fragment.split("&")[4].split("=")[1]
            logger.debug(access_token)
            logger.debug(refresh_token)
