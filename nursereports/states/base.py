
from ..server.supabase.auth import supabase_get_new_access_token
from ..server.supabase.user import supabase_get_user_info
from typing import Literal

import jwt
import os
import reflex as rx
import rich
import time

from dotenv import load_dotenv
from loguru import logger
from typing import Callable, Iterable

load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")

class BaseState(rx.State):

    access_token: str = rx.Cookie(
        name="access_token",
        same_site='strict',
        secure=True,
    )
    refresh_token: str = rx.Cookie(
        name="refresh_token",
        same_site='strict',
        secure=True,
    )
    user_info: dict
    
    @rx.cached_var
    def user_claims(self) -> dict:
        """Ensures that claims are valid and unexpired.

        Returns:
            dict:
                valid: bool
                payload: dict of claims if valid
                reason: if claims invalid - why
        """
        if self.access_token:
            try:
                claims = jwt.decode(
                    self.access_token,
                    jwt_key,
                    audience='authenticated',
                    algorithms=['HS256'],
                )
                return {
                    "valid": True,
                    "payload": claims,
                    "reason": None
                }
            except jwt.ExpiredSignatureError:
                return {
                    "valid": False,
                    "payload": None,
                    "reason": "expired"
                }
            except jwt.InvalidSignatureError:
                return {
                    "valid": False,
                    "payload": None,
                    "reason": "invalid"
                }
        else:
            return {
                "valid": False,
                "payload": None,
                "reason": "empty"
            }

    @rx.cached_var
    def user_is_authenticated(self) -> bool:
        if self.access_token:
            if self.user_claims['valid']:
                return True
            else:
                return False
        else:
            return False
        
    @rx.cached_var
    def user_has_reported(self) -> bool:
        if self.access_token and self.user_info:
            if self.user_info['needs_onboard']:
                return False
            else:
                return True
        else:
            return False

    def refresh_claims_if_needed(self) -> None:
        if self.access_token:
            if self.user_claims['valid']:
                current_time = int(time.time())
                expires_at = self.user_claims['payload']['exp']
                time_left_sec = (expires_at - current_time)
                if 5 <= time_left_sec <= 1800:
                    self.refresh_access_token()

    def refresh_access_token(self) -> None:
        response = supabase_get_new_access_token(
            self.access_token,
            self.refresh_token
        )
        if response["success"]:
            self.access_token = response["payload"]["access_token"]
            self.refresh_token = response["payload"]["refresh_token"]

    def user_access_granted(self, access_level) -> dict[bool, str]:
        """Returns dict containing access bool, and reason if denied.
        
        Args:
            access_level: 'login' or 'report' depending on what user 
                needs in order to access.

        Returns:
            dict:
                access_granted: bool
                reason: 'login' or 'report' depending on what the user was
                    missing.
        """
        if access_level == 'login' and not self.user_is_authenticated:
            return {
                "access_granted": False,
                "reason": "login"
            }
        if access_level == 'report' and not self.user_has_reported:
            if self.user_is_authenticated:
                return {
                    "access_granted": False,
                    "reason": "report"
                }
            else:
                return {
                    "access_granted": False,
                    "reason": "login"
                }
        return {
            "access_granted": True,
            "reason": None
        }

    def check_if_sso_redirect(self) -> Iterable[Callable]:
        from ..states.navbar import NavbarState
        raw_path = self.router.page.raw_path
        if ("access_token" in raw_path) and ("refresh_token" in raw_path):
            self.set_tokens_from_sso_redirect(raw_path)
            self.set_user_data()
            yield NavbarState.set_show_login

    def set_tokens_from_sso_redirect(self, raw_path) -> None:
        fragment = raw_path.split("#")[1]
        self.access_token = fragment.split("&")[0].split("=")[1]
        self.refresh_token = fragment.split("&")[4].split("=")[1]

    def set_user_data(self) -> None:
        response = supabase_get_user_info(self.access_token)
        if response['success']:
            self.user_info = response['payload']

    def redirect_if_access_denied(self, access_req) -> Iterable[Callable]:
        from ..states.navbar import NavbarState
        status = self.user_access_granted(access_req)
        if not status['access_granted']:
            if status['reason'] == 'login':
                yield rx.redirect('/')
                yield NavbarState.set_login_tab("login")
                yield NavbarState.set_show_login(True)
                yield NavbarState.set_error_sign_in_message(
                    "You must be logged in to access that content."
                )
            elif status['reason'] == 'report':
                yield rx.redirect('/onboard')
                yield NavbarState.set_alert_message(
                    "Please submit a report before accessing that content."
                )
            else:
                return rx.redirect('/')

    def event_state_standard_flow(
            self,
            access_req: Literal['none', 'login', 'report']
            ) -> Iterable[Callable] | None:
        """Simple standard login flow.
            1: Check if we are coming from an auth redirect.
            2: Refresh our claims if user is active and between 30-59 min.
            3: Redirect our user if they don't have proper access.

            Args:
                access_req: 'none', 'login', or 'report'
        """
        yield from self.check_if_sso_redirect()
        self.refresh_claims_if_needed()
        yield from self.redirect_if_access_denied(access_req)