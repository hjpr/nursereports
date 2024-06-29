from ..server.exceptions import (
    DuplicateUserError,
    PageRequiresLogin,
    ReadError,
    RequestFailed,
    TokenRefreshFailed,
    UserMissingReport,
)
from ..server.secrets import jwt_key
from ..server.supabase import (
    supabase_create_initial_user_info,
    supabase_get_new_access_token,
    supabase_get_user_info,
    supabase_get_user_modified_at_timestamp,
    supabase_get_user_reports,
    supabase_populate_saved_hospital_details,
    supabase_update_user_info,
)

from loguru import logger
from typing import Any, Dict, Callable, Iterable

import json
import jwt
import reflex as rx
import rich
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

    def event_state_standard_flow(self, access_level: str) -> Iterable[Callable]:
        """
        Simple standard login flow. Runs on_load prior to every page.

        This process ensures that:
            1: User claims are valid.
            2: User info is present.
            3: User is where they are allowed to be.

        Args:
            access_level: 'none', 'login', or 'report'
        """
        if self.user_claims["valid"] and self.user_info:
            return BaseState.authenticated_flow(access_level)
        if self.user_claims["valid"] and not self.user_info:
            return BaseState.authenticated_missing_info_flow(access_level)
        if not self.user_claims["valid"]:
            return BaseState.unauthenticated_flow(access_level)

    def event_state_refresh_user_info(self) -> Iterable[Callable]:
        """
        Use to load or refresh current user info. Runs on_load when opening the dashboard,
        ensuring that all the user values are up to date with the backend.
        """
        try:
            if self.check_user_data_has_updated():
                self.set_all_user_data()
            else:
                logger.debug("User information and database are in sync.")
        except (
            DuplicateUserError,
            ReadError,
            RequestFailed,
        ):
            yield rx.redirect("/logout/error")

    def authenticated_flow(self, access_level: str) -> Iterable[Callable] | None:
        """
        User is authenticated and user info is  present. Just make sure that
        user is accessing the appropriate resources for their access_level.
        """
        try:
            self.check_claims_for_expiring_soon()
            self.check_access(access_level)
        except TokenRefreshFailed as e:
            yield rx.toast.error(str(e))
        except PageRequiresLogin as e:
            yield rx.toast.error(str(e))
            yield rx.redirect("/")
        except UserMissingReport as e:
            yield rx.toast.error(str(e))
            yield rx.redirect("/onboard")

    def authenticated_missing_info_flow(
        self, access_level: str
    ) -> Iterable[Callable] | None:
        """
        User is authenticated but user info not present. After retrieving user
        data, make sure user is accessing appropriate resources for their
        access_level.
        """
        try:
            self.check_claims_for_expiring_soon()
            self.set_all_user_data()
            self.check_access(access_level)
            yield BaseState.redirect_user_to_onboard_or_dashboard
        except DuplicateUserError:
            yield rx.redirect("/logout/error")
        except PageRequiresLogin as e:
            yield rx.toast.error(str(e))
            yield rx.redirect("/")
        except ReadError as e:
            yield rx.toast.error(str(e))
        except RequestFailed:
            yield rx.toast.error("Unable to connect to backend.")
        except TokenRefreshFailed as e:
            yield rx.toast.error(str(e))
        except UserMissingReport as e:
            yield rx.toast.error(str(e))
            yield rx.redirect("/onboard")

    def unauthenticated_flow(self, access_level: str) -> Iterable[Callable]:
        """
        User is not authenticated, and is either just browsing the index page, or
        may be attempting to login using an SSO redirect. If coming from SSO then
        process the JWT and set the user data.
        """
        if self.user_claims["reason"] == "empty":
            yield BaseState.handle_sso_redirect
        if self.user_claims["valid"]:
            yield BaseState.authenticated_missing_info_flow

    def check_claims_for_expiring_soon(self) -> None:
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
            raise PageRequiresLogin("Login before accessing this page.")
        if access_level == "report" and not self.user_has_reported:
            if self.user_is_authenticated:
                raise UserMissingReport("Submit a report before accessing this page.")
            else:
                raise PageRequiresLogin("Login before accessing this page.")

    def handle_sso_redirect(self) -> Iterable[Callable]:
        try:
            raw_path = self.router.page.raw_path
            if ("access_token" in raw_path) and ("refresh_token" in raw_path):
                fragment = raw_path.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]
        except Exception:
            yield rx.toast.error("Invalid URL format for login.")

    def check_user_data_has_updated(self) -> bool:
        """
        Compare timestamp in database vs state. This check saves database pulls when
        user infomation hasn't changed and user lands on dashboard page.
        """
        access_token = self.access_token
        database_timestamp = supabase_get_user_modified_at_timestamp(access_token)[
            "modified_at"
        ]
        state_timestamp = self.user_info["modified_at"]
        logger.debug(
            f"Comparing db to state timestamps - {database_timestamp} {state_timestamp}"
        )
        return False if database_timestamp == state_timestamp else True

    def set_all_user_data(self) -> None:
        if self.user_claims["valid"]:
            self.set_user_info()
            self.set_saved_hospitals()
            self.set_user_reports()

    def set_user_info(self) -> None:
        user_info = supabase_get_user_info(self.access_token)
        if user_info:
            logger.debug("Setting user data from payload.")
            self.user_info = user_info
        else:
            self.create_new_user()

    def create_new_user(self) -> None:
        supabase_create_initial_user_info(
            self.access_token, self.user_claims["payload"]["sub"]
        )
        user_info = supabase_get_user_info(self.access_token)
        if user_info:
            self.user_info = user_info
        else:
            raise ReadError("User created, but failed to pull data after operation.")

    def set_saved_hospitals(self) -> None:
        hosp_list = self.user_info["saved_hospitals"]
        if hosp_list:
            saved_hospitals = supabase_populate_saved_hospital_details(
                self.access_token, hosp_list
            )
            self.saved_hospitals = saved_hospitals
        else:
            logger.warning("User doesn't have any saved hospitals to retrieve.")

    def event_state_add_hospital(self, hosp_id: str) -> Iterable[Callable]:
        try:
            if len(self.user_info["saved_hospitals"]) >= 30:
                yield rx.toast.error("Maximum number of saved hospitals reached. (30)")
            elif hosp_id not in self.user_info["saved_hospitals"]:
                new_user_info = self.user_info["saved_hospitals"] + [hosp_id]
                user_info = {"saved_hospitals": new_user_info}
                yield BaseState.update_user_info(user_info)
                yield rx.toast.success("Hospital saved to 'My Hospitals'.")
            else:
                yield rx.toast.warning("Hospital is already added to your list.")
        except RequestFailed as e:
            yield rx.toast.error(str(e), timeout=5000)

    def event_state_remove_set_hospital(self, hosp_id: str) -> Iterable[Callable]:
        new_user_info = [
            h for h in self.user_info["saved_hospitals"] if h != hosp_id
        ]
        user_info = {"saved_hospitals": new_user_info}
        yield BaseState.update_user_info(user_info)
        new_saved_hospitals = [
            h for h in self.saved_hospitals if h.get("hosp_id") != hosp_id
        ]
        self.saved_hospitals = new_saved_hospitals

    def set_user_reports(self) -> None:
        user_reports = supabase_get_user_reports(
            self.access_token, self.user_claims["payload"]["sub"]
        )
        if user_reports:
            self.user_reports = user_reports
        else:
            logger.warning("Retrieved empty list when requesting user reports.")

    def update_user_info(self, user_data: Dict[Any, Any]) -> Iterable[Callable]:
        """
        Wraps the supabase request to update user data so that if successful, whatever
        data gets written to supabase, also gets written back to user_info to maintain
        consistency from state <-> database.

        Args:
            user_data: dict - data to be written
        """
        try:
            updated_data = supabase_update_user_info(
                self.access_token, self.user_claims["payload"]["sub"], user_data
            )
            self.user_info.update(updated_data)
        except RequestFailed as e:
            yield rx.toast.error(str(e))


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
