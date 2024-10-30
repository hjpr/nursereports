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
    supabase_delete_user_report,  # Uncomment when ready to use function.
    supabase_get_new_access_token,
    supabase_get_user_info,
    supabase_get_user_modified_at_timestamp,
    supabase_get_user_reports,
    supabase_populate_saved_hospital_details,
    supabase_update_user_info,
)

from datetime import datetime
from loguru import logger
from typing import Callable, Iterable

import jwt
import reflex as rx
import time
import rich


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
    user_info: dict[str, any] = {}
    saved_hospitals: list[dict[str, str]] = []

    @rx.var
    def host_address(self) -> str:
        return self.router.page.host

    @rx.var
    def reason_for_logout(self) -> str:
        return self.router.page.params.get("logout_reason")

    @rx.var
    def user_claims(self) -> dict[str, str]:
        """
        Pull claims from JWT if valid, authenticated, and not expired.
        """
        try:
            if self.access_token:
                claims = jwt.decode(
                    self.access_token,
                    jwt_key,
                    audience="authenticated",
                    algorithms=["HS256"],
                )
                return claims
            else:
                return {}

        except Exception as e:
            logger.critical(e)
            return {}

    @rx.var(cache=True)
    def user_claims_id(self) -> str | None:
        return self.user_claims.get("sub", None)

    @rx.var(cache=True)
    def user_claims_email(self) -> str | None:
        return self.user_claims.get("email", None)

    @rx.var(cache=True)
    def user_claims_issued_by(self) -> str | None:
        return self.user_claims.get("iss", None)

    @rx.var(cache=True)
    def user_claims_issued_at(self) -> int | None:
        return self.user_claims.get("iat", None)

    @rx.var(cache=True)
    def user_claims_expires_at(self) -> int:
        return self.user_claims.get("exp", int(time.time()))

    @rx.var
    def user_claims_expiring(self) -> bool:
        current_time = int(time.time)
        expires_at = self.user_claims_expires_at
        seconds_to_expiration = expires_at - current_time
        return True if seconds_to_expiration <= 900 else False

    @rx.var(cache=True)
    def user_claims_authenticated(self) -> bool:
        return True if self.user_claims.get("aud") == "authenticated" else False

    @rx.var(cache=True)
    def user_has_reported(self) -> bool:
        return self.user_info.get("needs_onboard", False)

    def event_state_standard_flow(self) -> Iterable[Callable]:
        """
        Simple standard login flow. Runs on_load prior to every page.
        """
        # If user is authenticated.
        if self.user_claims_authenticated:
            # Ensure expiring access tokens are refreshed.
            if self.user_claims_expiring and (self.access_token and self.refresh_token):
                self.refresh_access_token()

            # Ensure user data is present and current.
            if not (self.user_info and self.local_user_data_synced_with_remote()):
                yield from self.reset_user_info()

        # If user is not authenticated.
        if not self.user_claims_authenticated:
            # User claims are expired
            if self.access_token or self.refresh_token:
                self.access_token = ""
                self.refresh_token = ""
                yield rx.redirect("/")
                yield rx.toast.info("Login expired, please login again.")

            # User coming from an SSO redirect.
            url = self.router.page.raw_path
            if ("access_token" in url) and ("refresh_token" in url):
                yield rx.toast.info("Logging you in...")
                fragment = url.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]
                yield rx.redirect("/dashboard")

    def refresh_access_token(self) -> None:
        """
        Refresh JWT token using refresh token.
        """
        access_token = self.access_token
        refresh_token = self.refresh_token
        tokens = supabase_get_new_access_token(access_token, refresh_token)
        self.access_token = tokens.get("access_token", "")
        self.refresh_token = tokens.get("refresh_token", "")

    def local_user_data_synced_with_remote(self) -> bool:
        """
        Check modified_at timestamps to ensure user_info is in sync.
        """
        remote_modified_at_timestamp = supabase_get_user_modified_at_timestamp(
            self.access_token
        )["modified_at"]
        local_modified_at_timestamp = self.user_info.get("modified_at", None)
        return (
            True
            if remote_modified_at_timestamp == local_modified_at_timestamp
            else False
        )

    def reset_user_info(self) -> Iterable[Callable]:
        """
        Resets exising user's info, or creates new user if user info missing.
        """
        try:
            # Set user info to state or create new user
            user_info = supabase_get_user_info(self.access_token)
            if user_info:
                self.user_info = user_info
            else:
                yield from self.create_new_user()

            # Set saved hospitals to state.
            saved_hospitals = supabase_populate_saved_hospital_details(
                self.access_token, self.user_info.get("saved_hospitals", None)
            )

            # Format hospital names from all caps to .title case.
            if saved_hospitals:
                for hospital in saved_hospitals:
                    hospital["hosp_city"] = hospital["hosp_city"].title()
                self.saved_hospitals = saved_hospitals

            # Set user reports to state.
            user_reports = supabase_get_user_reports(
                self.access_token, self.user_claims_id
            )

            # Format user report timestamps
            if user_reports:
                for hospital in user_reports:
                    hospital["created_at"] = datetime.fromisoformat(
                        hospital["created_at"]
                    ).strftime("%Y - %B")
                    if hospital["modified_at"]:
                        hospital["modified_at"] = datetime.fromisoformat(
                            hospital["modified_at"]
                        ).strftime("%Y - %B")
            self.user_reports = user_reports

        except Exception as e:
            logger.critical(e)
            yield rx.redirect("/")
            yield rx.toast.error("Unable to reset user info.")

    def create_new_user(self) -> Iterable[Callable]:
        """
        Create new user in remote database and save to local state.
        """
        try:
            supabase_create_initial_user_info(self.access_token, self.user_claims_id)
            user_info = supabase_get_user_info(self.access_token)
            self.user_info = user_info
        except Exception as e:
            logger.critical(e)
            yield rx.toast.error("Unable to perform new user creation.")

    def update_user_info_and_sync_locally(
        self, data: dict[str, any]
    ) -> Iterable[Callable]:
        """
        Provide user info data to update to remote database, then save to local state.
        """
        try:
            updated_data = supabase_update_user_info(
                self.access_token, self.user_claims_id, data
            )
            self.user_info.update(updated_data)
        except Exception as e:
            logger.critical(e)
            yield rx.toast.error("Unable to perform requested update.")

    def event_state_add_hospital(self, hosp_id: str) -> Iterable[Callable]:
        try:
            if len(self.user_info["saved_hospitals"]) >= 30:
                yield rx.toast.error("Maximum number of saved hospitals reached. (30)")
            elif hosp_id not in self.user_info["saved_hospitals"]:
                new_user_info = self.user_info["saved_hospitals"] + [hosp_id]
                user_info = {"saved_hospitals": new_user_info}
                yield from self.update_user_info_and_sync_locally(user_info)
                yield rx.toast.success("Hospital saved to 'My Hospitals'.")
            else:
                yield rx.toast.warning("Hospital is already added to your list.")
        except RequestFailed as e:
            yield rx.toast.error(str(e), timeout=5000)
        except Exception as e:
            logger.critical(str(e))

    def event_state_remove_hospital(self, hosp_id: str) -> Iterable[Callable]:
        try:
            new_user_info = [
                h for h in self.user_info["saved_hospitals"] if h != hosp_id
            ]
            user_info = {"saved_hospitals": new_user_info}
            self.update_user_info_and_sync_locally(user_info)
            new_saved_hospitals = [
                h for h in self.saved_hospitals if h.get("hosp_id") != hosp_id
            ]
            self.saved_hospitals = new_saved_hospitals
        except RequestFailed as e:
            yield rx.toast.error(str(e))
        except Exception as e:
            logger.critical(str(e))

    def event_state_remove_report(self, report_id: str) -> Iterable[Callable]:
        try:
            logger.critical(f"Attempting to remove {report_id}")
            # updated_user_reports= [h for h in self.user_reports if report_id != h["report_id"]]
            # supabase_delete_user_report(self.access_token, report_id)
            # self.user_reports = updated_user_reports
            yield rx.toast.success("Removed report from our database.")
        except RequestFailed as e:
            yield rx.toast.error(str(e))
        except Exception as e:
            logger.critical(str(e))

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

    def redirect_user_to_onboard_or_dashboard(self) -> Callable:
        if self.user_has_reported:
            return rx.redirect("/dashboard")
        else:
            return rx.redirect("/onboard")

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
