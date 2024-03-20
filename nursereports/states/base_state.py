from ..server.secrets import jwt_key
from ..server.supabase import (
    supabase_create_initial_user_info,
    supabase_get_new_access_token,
    supabase_get_user_info
)

from loguru import logger
from typing import Callable, Iterable

import inspect
import jwt
import reflex as rx
import rich
import time

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

    @rx.var
    def reason_for_logout(self) -> str:
        return self.router.page.params.get('logout_reason')
    
    @rx.cached_var
    def user_claims(self) -> dict:
        """Pull claims from JWT if valid and not expired.

        Returns:
            dict:
                valid: bool
                payload: dict of claims if valid
                reason: if claims invalid, 'expired', 'invalid',
                    or 'empty'

        Payload contains:
            aud: role 'authenticated' if valid
            exp: unix timestamp of expiration
            iat: unix timestamp of issue
            iss: issuer of jwt
            sub: user id as uuid
            email: <-
            phone: <-
            app_metadata: stuff like methods of login
            user_metadata: useful store of small info
            role: 'authenticated' unless change to role system
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

    def check_claims_for_expiring_soon(self) -> None:
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

    def user_access_granted(self, access_level) -> dict:
        """Returns dict containing access bool, and reason if denied.
        
        Args:
            access_level: 'login' or 'report' depending on what user 
                needs in order to access.

        Returns:
            dict:
                granted: bool
                reason: 'login' or 'report' depending on what the user was
                    missing.
        """
        if access_level == 'login' and not self.user_is_authenticated:
            logger.warning(inspect.cleandoc(
                f"""{self.router.session.client_ip} attempted to access
                resources requiring login."""
            ))
            return {
                "granted": False,
                "reason": "login"
            }
        if access_level == 'report' and not self.user_has_reported:
            if self.user_is_authenticated:
                logger.warning(inspect.cleandoc(
                    f"""{self.user_claims['payload']['sub']} attempted
                    to access resources requiring report."""
                ))
                return {
                    "granted": False,
                    "reason": "report"
                }
            else:
                logger.warning(inspect.cleandoc(
                    f"""{self.router.session.client_ip} attempted to
                    access resources requiring login."""
                ))
                return {
                    "granted": False,
                    "reason": "login"
                }
        return {
            "granted": True,
            "reason": None
        }

    def event_state_standard_flow(self, access_req: str
        ) -> Iterable[Callable]:
        """
        Simple standard login flow.
            If claims are valid and user info present:
                User is logged in, so check if they have
                reported or not and refresh token as needed.
            If claims are valid but no user info:
                Set user info from public entry in /users,
                create an entry if entry doesn't exist,
                or kick out to error if not possible.
                possible.
            If claims aren't valid:
                Check claims reason and redirect accordingly.

        This process ensures that:
            1: User claims are valid
            2: User info is present
            3: User is where they are allowed to be

        Args:
            access_req: 'none', 'login', or 'report'

        Context:
            Yields to on_load event handler
        """
        if self.user_claims['valid'] and self.user_info:
            self.check_claims_for_expiring_soon()
            yield from self.redirect_if_access_denied(access_req)
        elif self.user_claims['valid'] and not self.user_info:
            response = self.set_user_data()
            if response['success']:
                self.check_claims_for_expiring_soon()
                yield from self.redirect_if_access_denied(access_req)
            else:
                yield rx.redirect('/logout/error')
        else:
            if self.user_claims['reason'] == 'empty':
                yield from self.check_if_sso_redirect()
                yield from self.redirect_if_access_denied(access_req)
            if self.user_claims['reason'] == 'expired':
                yield rx.redirect('/logout/expired')
            if self.user_claims['reason'] == 'invalid':
                yield rx.redirect('/logout/error')

    def check_if_sso_redirect(self) -> Iterable[Callable]:
        raw_path = self.router.page.raw_path
        if ("access_token" in raw_path) and ("refresh_token" in raw_path):
            self.set_tokens_from_sso_redirect(raw_path)
            response = self.set_user_data()
            if response['success']:
                yield from self.redirect_for_report_status()
            else:
                yield rx.redirect('/logout/error')

    def set_tokens_from_sso_redirect(self, raw_path) -> None:
        logger.debug(
            "Coming from SSO redirect. Parsing URL for tokens."
        )
        fragment = raw_path.split("#")[1]
        self.access_token = fragment.split("&")[0].split("=")[1]
        self.refresh_token = fragment.split("&")[4].split("=")[1]

    def set_user_data(self) -> dict:
        """
        Attempts to pull user data from supabase. If first time and 
        user has no info, will create entry in public/users with default
        values.

        Returns:
            dict:
                success: bool
                status: user readable reason for failure

        Context:
            If we have to create a user entry, we don't need to retrieve it
            afterwards because we know the defaults that supabase writes.
        """
        response = supabase_get_user_info(self.access_token)
        if response['success']:
            logger.debug("Setting user data from payload.")
            self.user_info = response['payload']
            return response
        elif not response['success'] and response['status'] == \
            "No user info present":
            response = supabase_create_initial_user_info(
                self.access_token,
                self.user_claims['payload']['sub']
            )
            if response['success']:
                logger.debug("Setting user info to default values.")
                self.user_info = {
                    "uuid": self.user_claims['payload']['sub'],
                    "license": "",
                    "license_state": "",
                    "membership": "free",
                    "needs_onboard": True,
                    "my_hospitals": {},
                    "my_jobs": {},
                    "trust": 0
                }
                return response
            else:
                logger.critical("Unable to set up first time user!")
                rich.inspect(response)
                return response
        else:
            return response

    def redirect_for_report_status(self) -> Iterable[Callable]:
        if self.user_has_reported:
            yield rx.redirect('/dashboard')
        else:
            yield rx.redirect('/onboard')

    def redirect_if_access_denied(self, access_req) -> Iterable[Callable]:
        from .navbar_state import NavbarState
        access = self.user_access_granted(access_req)
        if not access['granted']:
            if access['reason'] == 'login':
                yield rx.redirect('/')
                yield NavbarState.set_login_tab("login")
                yield NavbarState.set_show_login(True)
                yield NavbarState.set_error_sign_in_message(
                    "You must be logged in to access that content."
                )
            elif access['reason'] == 'report':
                yield rx.redirect('/onboard')
                yield NavbarState.set_alert_message(
                    "Please submit a report before accessing that content."
                )
            else:
                yield rx.redirect('/')

    def event_state_logout(self) -> Iterable[Callable]:
        from . import NavbarState
        if self.reason_for_logout == 'user':
            self.reset()
            yield NavbarState.set_alert_message("Successfully logged out.")
        if self.reason_for_logout == 'error':
            logger.critical(
                "Logged user out forcefully - probably server error."
            )
            self.reset()
            yield NavbarState.set_alert_message(inspect.cleandoc("""Encountered error requiring reset.
                If this message persists, the backend is likely down
                and we are in the process of recovering.
                """))
        if self.reason_for_logout == 'expired':
           self.reset()
           yield NavbarState.set_alert_message("""For your security, you've been
                logged out for inactivity.
                """)
        yield rx.redirect('/')