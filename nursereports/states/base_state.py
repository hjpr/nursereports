from ..server.exceptions import (
    DuplicateUserError,
    ExpiredError,
    LoginError,
    ReadError,
    ReportError,
    RequestError,
    TokenError,
)
from ..server.secrets import jwt_key
from ..server.supabase import (
    supabase_create_initial_user_info,
    supabase_get_new_access_token,
    supabase_get_saved_hospitals,
    supabase_get_user_info,
    supabase_get_user_modified_at_timestamp,
    supabase_get_user_reports,
)

from loguru import logger
from typing import Callable, Iterable

import jwt
import reflex as rx
import time


class BaseState(rx.State):
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

    user_info: dict = {}
    saved_hospitals: list[dict] = []
    user_reports: list[dict] = []

    @rx.var
    def host_address(self) -> str:
        return self.router.page.host

    @rx.var
    def reason_for_logout(self) -> str:
        return self.router.page.params.get("logout_reason")

    @rx.cached_var
    def user_claims(self) -> dict:
        """Pull claims from JWT if valid, authenticated, and not expired.

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
                    audience="authenticated",
                    algorithms=["HS256"],
                )
                return {"valid": True, "payload": claims, "reason": None}
            except jwt.ExpiredSignatureError:
                return {"valid": False, "payload": None, "reason": "expired"}
            except jwt.InvalidSignatureError:
                return {"valid": False, "payload": None, "reason": "invalid"}
        else:
            return {"valid": False, "payload": None, "reason": "empty"}

    @rx.cached_var
    def user_is_authenticated(self) -> bool:
        if self.access_token:
            if self.user_claims["valid"]:
                return True
            else:
                return False
        else:
            return False

    @rx.cached_var
    def user_has_reported(self) -> bool:
        if self.access_token and self.user_info:
            if self.user_info["needs_onboard"]:
                return False
            else:
                return True
        else:
            return False

    @rx.cached_var
    def user_has_saved_hospitals(self) -> bool:
        if self.access_token and self.user_info:
            if self.user_info["saved_hospitals"]:
                return True
            else:
                return False

    def event_state_standard_flow(self, access_level: str) -> Iterable[Callable]:
        """
        Simple standard login flow. Runs on_load prior to every page.

        This process ensures that:
            1: User claims are valid.
            2: User info is present and dashboard info is populated.
            3: User is where they are allowed to be.

        Args:
            access_level: 'none', 'login', or 'report'
        """
        try:
            if self.user_claims["valid"] and self.user_info:
                self.authenticated_flow(access_level)
            if self.user_claims["valid"] and not self.user_info:
                self.authenticated_missing_info_flow(access_level)
            if not self.user_claims["valid"]:
                self.unauthenticated_flow(access_level)
        except ExpiredError:
            yield rx.redirect("/logout/expired")
        except LoginError:
            yield from self.redirect_user_to_login()
        except ReportError:
            yield from self.redirect_user_to_onboard()
        except (
            DuplicateUserError,
            RequestError,
            TokenError,
        ) as e:
            error_message = str(e)
            yield rx.toast.error(error_message, timeout=5000)
            yield rx.redirect("/logout/error")

    def event_state_refresh_user_info(self) -> Iterable[Callable]:
        """
        Use to load or refresh current user info. Runs on_load when opening the dashboard,
        ensuring that all the user values are up to date with the backend.
        """
        try:
            if self.check_user_data_has_updated:
                self.set_all_user_data()
        except (
            DuplicateUserError,
            ReadError,
            RequestError,
        ) as e:
            error_message = str(e)
            yield rx.toast.error(error_message, timeout=5000)
            yield rx.redirect("/logout/error")

    def authenticated_flow(self, access_level: str) -> None:
        """
        User is authenticated and user info is present. Just make sure that
        user is accessing the appropriate resources for their access_level.
        """
        self.check_claims_for_expiring_soon()
        self.check_access(access_level)

    def authenticated_missing_info_flow(self, access_level: str) -> None:
        """
        User is authenticated but user info not present. After retrieving user
        data, make sure user is accessing appropriate resources for their
        access_level.
        """
        self.check_claims_for_expiring_soon()
        self.set_all_user_data()
        self.check_access(access_level)

    def unauthenticated_flow(self, access_level: str) -> None:
        """
        User is not authenticated, and is either just browsing the index page, or
        may be attempting to login using an SSO redirect. If coming from SSO then
        process the JWT, set the user data, and make sure user is accessing
        appropriate resouces for their access_level.
        """
        if self.user_claims["reason"] == "empty":
            self.handle_sso_redirect()
        if self.user_claims["valid"]:
            self.authenticated_missing_info_flow

    def check_claims_for_expiring_soon(self) -> None:
        """
        Refreshes access token. If access token expires, then site will
        log user out for inactivity.
        """
        current_time = int(time.time())
        expires_at = self.user_claims["payload"]["exp"]
        time_left_sec = expires_at - current_time
        if 5 <= time_left_sec <= 1800:
            self.refresh_access_token()

    def refresh_access_token(self) -> None:
        access_token = self.access_token
        refresh_token = self.refresh_token
        tokens = supabase_get_new_access_token(access_token, refresh_token)
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]

    def check_access(self, access_level: str) -> None:
        if access_level == "login" and not self.user_is_authenticated:
            raise LoginError("Login before accessing this page.")
        if access_level == "report" and not self.user_has_reported:
            if self.user_is_authenticated:
                raise ReportError("Submit a report before accessing this page.")
            else:
                raise LoginError("Login before accessing this page.")

    def handle_sso_redirect(self) -> None:
        raw_path = self.router.page.raw_path
        if ("access_token" in raw_path) and ("refresh_token" in raw_path):
            try:
                fragment = raw_path.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]
            except Exception:
                raise TokenError("Encountered an error processing JWT via SSO.")

    def check_user_data_has_updated(self) -> bool:
        """
        Compare timestamp in database vs state. This check saves database pulls when
        user infomation hasn't changed and user lands on dashboard page.
        """
        access_token = self.access_token
        database_timestamp = supabase_get_user_modified_at_timestamp(access_token)
        state_timestamp = self.user_info["modified_at"]
        logger.debug(
            f"Comparing db to state timestamps - {database_timestamp} {state_timestamp}"
        )
        return False if database_timestamp == state_timestamp else True

    def set_all_user_data(self) -> None:
        """
        Calls three different functions to set user info, saved hospitals, and
        reviews. DONT USE THIS BY ITSELF. Needs to be set in a stack
        that catches exceptions from its referenced functions.
        """
        if self.user_claims["valid"]:
            access_token = self.access_token
            user_id = self.user_claims["payload"]["sub"]
            self.set_user_info(access_token, user_id)
            self.set_saved_hospitals(access_token, user_id)
            self.set_user_reports(access_token, user_id)

    def set_user_info(self, access_token: str, user_id: str) -> None:
        """
        Retrieves user info and saves to state. If no user info present
        creates entry in database.
        """
        user_info = supabase_get_user_info(access_token)
        if user_info:
            logger.debug("Setting user data from payload.")
            self.user_info = user_info
        else:
            self.create_new_user(access_token, user_id)

    def create_new_user(self, access_token: str, user_id: str) -> None:
        """
        Creates a new user in database and saves that user info to state.
        """
        supabase_create_initial_user_info(access_token, user_id)
        user_info = supabase_get_user_info(access_token)
        if user_info:
            logger.debug("Setting user data from payload.")
            self.user_info = user_info
        else:
            raise ReadError("Created user data, but unable to pull that data afterwards.")

    def set_saved_hospitals(self, access_token, user_id) -> None:
        """
        Retrieves user's saved hospitals from database and saves them to state.
        """
        saved_hospitals = supabase_get_saved_hospitals(access_token, user_id)
        if saved_hospitals:
            logger.debug("Setting saved hospitals into state.")
            self.saved_hospitals = saved_hospitals
        else:
            logger.debug("User doesn't have any saved hospitals to retrieve.")

    def set_user_reports(self, access_token, user_id) -> None:
        """
        Retrieves user reports from database and saves them to state.
        """
        user_reports = supabase_get_user_reports(access_token, user_id)
        if user_reports:
            logger.debug("Setting user reports into state.")
            self.user_reports = user_reports
        else:
            logger.warning("Retrieved empty list when requesting user reports.")

    def redirect_user_to_login(self) -> Iterable[Callable]:
        from .navbar_state import NavbarState

        yield rx.redirect("/")
        yield NavbarState.set_login_tab("login")
        yield NavbarState.set_show_login(True)
        yield NavbarState.set_error_sign_in_message(
            "You must be logged in to access that content."
        )

    def redirect_user_to_onboard(self) -> Iterable[Callable]:
        from .navbar_state import NavbarState

        yield rx.redirect("/onboard")
        yield NavbarState.set_alert_message(
            "Please submit a report before accessing that content."
        )

    def redirect_user_to_onboard_or_dashboard(self) -> Iterable[Callable]:
        if self.user_has_reported:
            yield rx.redirect("/dashboard")
        else:
            yield rx.redirect("/onboard")

    def event_state_logout(self) -> Iterable[Callable]:
        from . import NavbarState

        if self.reason_for_logout == "user":
            self.reset()
            yield NavbarState.set_alert_message("Successfully logged out.")
        if self.reason_for_logout == "error":
            self.reset()
            yield NavbarState.set_alert_message(
                """Encountered an error. If this message
                persists, please contact support@nursereports.org."""
            )
        if self.reason_for_logout == "expired":
            self.reset()
            yield NavbarState.set_alert_message(
                """For your security, you've been
                logged out for inactivity."""
            )
        yield rx.redirect("/")
