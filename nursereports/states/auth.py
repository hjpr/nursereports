
from ..events.auth import event_supabase_sso_login
from ..states.base import BaseState
from ..states.navbar import NavbarState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx

class AuthState(BaseState):
    @rx.var
    def auth_params(self):
        return self.router.page.params.get('auth_params')
        
    def event_state_sso_parse_params(self) -> Callable:
        if "sso" in self.auth_params:
            fragment = self.auth_params.split("#")[1]
            access_token = fragment.split("&")[0].split("=")[1]
            refresh_token = fragment.split("&")[4].split("=")[1]
            self.access_token = access_token
            self.refresh_token = refresh_token
        return rx.redirect('/')
