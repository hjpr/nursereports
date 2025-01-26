from ..server.exceptions import RequestFailed
from ..server.mailgun import mailgun_send_email
from ..server.secrets import api_url, jwt_key
from ..server.supabase import (
    supabase_create_initial_user_info,
    supabase_create_account_with_email,
    supabase_delete_user_report,
    supabase_get_hospital_info,
    supabase_get_user_info,
    supabase_get_user_modified_at_timestamp,
    supabase_get_user_reports,
    supabase_login_with_email,
    supabase_populate_saved_hospital_details,
    supabase_recover_password,
    supabase_update_user_info,
)
from ..states.auth_state import AuthState

from datetime import datetime
from loguru import logger
from typing import Callable, Iterable

import jwt
import pprint
import reflex as rx
import time


class UserState(AuthState):
    # Stored dict of user information from /public.
    user_info: dict[str, str | list | dict | None] = {}

    # Stored list of user information from /public
    user_reports: list[dict[str, str]] = []

    # Stored list of user information from /public
    user_saved_hospitals: list[dict[str, str]] = []

    # Used to display loading wheel for user UI events.
    user_is_loading: bool = False

    # Limit the rate at which a user can send contact.
    user_contact_email_time: int = 0

    # Limit rate at which user can send password recovery.
    user_recovery_email_time: int = 0

    @rx.var(cache=True)
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
        return self.user_claims.get("sub")

    @rx.var(cache=True)
    def user_claims_email(self) -> str | None:
        return self.user_claims.get("email")

    @rx.var(cache=True)
    def user_claims_issued_by(self) -> str | None:
        return self.user_claims.get("iss")

    @rx.var(cache=True)
    def user_claims_issued_at(self) -> int | None:
        return self.user_claims.get("iat")

    @rx.var(cache=True)
    def user_claims_expires_at(self) -> int | None:
        return self.user_claims.get("exp")

    @rx.var(cache=True)
    def user_claims_authenticated(self) -> bool:
        return True if self.user_claims.get("aud") == "authenticated" else False

    @rx.var(cache=True)
    def user_has_reported(self) -> bool:
        reports_submitted = len(self.user_info.get("reports", {}).get("ids", {}))
        return True if reports_submitted > 0 else False

    @rx.var(cache=True)
    def user_claims_expiring(self) -> bool:
        if self.user_claims_authenticated:
            current_time = int(time.time())
            expires_at = self.user_claims_expires_at
            seconds_to_expiration = expires_at - current_time
            return True if seconds_to_expiration <= 900 else False
        return False

    def event_state_submit_login(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the login page.
        """
        try:
            # Disable login attempts while request is out.
            self.user_is_loading = True

            if auth_data.get("email") and auth_data.get("password"):
                # Grab auth data from form submission.
                email = auth_data.get("email")
                password = auth_data.get("password")

                # Get JWT using provided auth data.
                tokens = supabase_login_with_email(email, password)
                self.access_token = tokens.get("access_token")

                # Get user data.
                self.get_user_info()

                # Send to proper page.
                yield from self.redirect_user_to_onboard_or_dashboard()

            # If either email or password are missing.
            else:
                yield rx.toast.error("Both fields are required.")

            # Re-enable login attempts after requests.
            self.user_is_loading = False

        except Exception as e:
            logger.warning(e)
            yield rx.toast.error(e)
            self.user_is_loading = False

    def event_state_create_account(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the create-account page.
        """
        try:
            self.user_is_loading = True

            if (
                auth_data.get("create_account_email")
                and auth_data.get("create_account_password")
                and auth_data.get("create_account_password_confirm")
            ):
                # Grab auth data from form submission.
                email = auth_data.get("create_account_email")
                password = auth_data.get("create_account_password")
                password_confirm = auth_data.get("create_account_password_confirm")

                # Check if passwords match
                if password != password_confirm:
                    self.user_is_loading = False
                    return rx.toast.error("Passwords do not match.", close_button=True)

                # Create account from auth data.
                supabase_create_account_with_email(email, password)

                # Reset variables and redirect to the link confirmation page.
                yield rx.redirect("/login/confirm")

            else:
                self.user_is_loading = False
                yield rx.toast.error("All fields must be completed.", close_button=True)

        except Exception as e:
            logger.error(e)
            yield rx.toast.error(str(e), close_button=True)
            self.user_is_loading = False

    def event_state_login_with_sso(self, provider: str) -> Iterable[Callable]:
        """
        Navigate to Supabase SSO endpoint.
        """
        try:
            self.user_is_loading = True

            # Supabase API endpoint for SSO auth.
            yield rx.redirect(f"{api_url}/auth/v1/authorize?provider={provider}")

            self.user_is_loading = False

        except Exception as e:
            logger.error(e)
            yield rx.toast.error(
                str(e),
                close_button=True,
            )
            self.user_is_loading = False

    def create_new_user(self) -> None:
        """
        Create new user in remote database and save to local state.
        """
        supabase_create_initial_user_info(self.access_token, self.user_claims_id)
        user_info = supabase_get_user_info(self.access_token)
        self.user_info = user_info

    def get_user_info(self) -> None:
        """
        Refreshes exising user's info in state, or creates new user if user info missing.
        """
        # Set user info to state or create new user
        user_info = supabase_get_user_info(self.access_token)
        if user_info:
            self.user_info = user_info
        else:
            self.create_new_user()

        # Get all users saved hospital information.
        self.get_user_saved_hospitals()

        # Get all user reports.
        self.get_user_reports()

    def get_user_saved_hospitals(self) -> None:
        """Get or refresh saved hospitals."""
        if self.user_info.get("saved_hospitals"):
            saved_hospitals = supabase_populate_saved_hospital_details(
                self.access_token, self.user_info.get("saved_hospitals")
            )

            # Format hospital cities from all caps to 'title' case.
            for hospital in saved_hospitals:
                hospital["hosp_city"] = hospital["hosp_city"].title()
            self.user_saved_hospitals = saved_hospitals
        else:
            self.user_saved_hospitals = []

    def get_user_reports(self) -> None:
        """Get or refresh user reports."""
        user_reports = supabase_get_user_reports(self.access_token, self.user_claims_id)

        if user_reports:
            for hospital in user_reports:
                # Get the city and state for each hospital.
                hospital_data = supabase_get_hospital_info(
                    self.access_token, hospital.get("hospital_id", "")
                )
                hospital["hosp_city"] = hospital_data.get("hosp_city", "").title()
                hospital["hosp_state"] = hospital_data.get("hosp_state", "")

                # Format timestamps as YYYY-MM
                if hospital["created_at"]:
                    hospital["created_at"] = datetime.fromisoformat(
                        hospital["created_at"]
                    ).strftime("%B %Y")
                if hospital["modified_at"]:
                    hospital["modified_at"] = datetime.fromisoformat(
                        hospital["modified_at"]
                    ).strftime("%B %Y")

        self.user_reports = user_reports

    def update_user_info_and_sync_locally(
        self, data: dict[str, any]
    ) -> Iterable[Callable]:
        """
        Provide user info data to update to remote database, then save to local state.
        """
        synced_data = supabase_update_user_info(
            self.access_token, self.user_claims_id, data
        )
        self.user_info.update(synced_data)
        pprint.pp(self.user_info)

    def local_user_data_synced_with_remote(self) -> bool:
        """
        Check modified_at timestamps to ensure user_info is in sync locally -> supabase.
        """
        remote_modified_at_timestamp = supabase_get_user_modified_at_timestamp(self.access_token)["modified_at"]
        local_modified_at_timestamp = self.user_info["modified_at"]
        return (
            True
            if remote_modified_at_timestamp == local_modified_at_timestamp
            else False
        )

    def event_state_add_hospital(self, hosp_id: str) -> Iterable[Callable]:
        """
        Add a user selected hospital to user's saved hospital list.
        """
        try:
            # Limit saved hospital list length to 30 items.
            if len(self.user_info["saved_hospitals"]) >= 30:
                yield rx.toast.error("Maximum number of saved hospitals reached. (30)")

            # If not duplicate, and not present in list, add to list.
            elif hosp_id not in self.user_info["saved_hospitals"]:
                new_user_info = self.user_info["saved_hospitals"] + [hosp_id]
                user_info = {"saved_hospitals": new_user_info}
                self.update_user_info_and_sync_locally(user_info)
                yield rx.toast.success("Hospital added to 'Saved Hospitals'.")

            # Notify user that hospital is already present.
            else:
                yield rx.toast.warning(
                    "This hospital has already been saved to your list."
                )

        except RequestFailed as e:
            yield rx.toast.error(str(e), timeout=5000)
        except Exception as e:
            logger.critical(str(e))
            yield rx.toast.error("Unable to save hospital to list.")

    def event_state_remove_hospital(self, hosp_id: str) -> Iterable[Callable]:
        """
        Removes a selected hospital from user's saved hospital list.
        """
        try:
            # Make a new list not including selected hospital.
            new_saved_hospitals = [
                h for h in self.user_info["saved_hospitals"] if h != hosp_id
            ]

            # Upload new list to cloud database.
            user_info = {"saved_hospitals": new_saved_hospitals}

            # Uploads and syncs data locally from remote database.
            self.update_user_info_and_sync_locally(user_info)

            # Repulls hospital info to update list.
            self.get_user_saved_hospitals()

            yield rx.toast.success("Hospital removed from 'Saved Hospitals'")

        except RequestFailed as e:
            yield rx.toast.error(str(e))
        except Exception as e:
            logger.critical(str(e))

    def event_state_remove_report(self, report_id: str) -> Iterable[Callable]:
        """
        Removes own user's report from database.
        """
        try:
            # Create new local list excluding the report to delete.
            updated_user_reports = [
                h for h in self.user_reports if report_id != h["report_id"]
            ]

            # Remove the report from the database.
            supabase_delete_user_report(self.access_token, report_id)

            # Update the local state with report list.
            self.user_reports = updated_user_reports

            yield rx.toast.success("Removed report from our database.")

        except RequestFailed as e:
            yield rx.toast.error(str(e))
        except Exception as e:
            logger.critical(str(e))

    def event_state_contact_us_submit(self, contact_dict: dict) -> Iterable[Callable]:
        """
        Submits info to email via contact us page. User must wait 5 min between submissions.
        """
        try:
            subject = contact_dict.get("subject")
            text = contact_dict.get("text")
            current_time = int(time.time())
            wait_interval = 300
            wait_time = int(current_time - wait_interval) - self.user_contact_email_time

            # Check that wait interval isn't sooner than 5 min.
            if wait_time >= 0:
                if subject and text:
                    yield mailgun_send_email(
                        "support@nursereports.org",
                        "jeremy.f.medlin@gmail.com",
                        subject,
                        text,
                    )
                    self.user_contact_email_time = current_time
                    yield rx.toast.success("Thanks for reaching out!")
                else:
                    yield rx.toast.error("Some or all required fields are empty.")

            else:
                yield rx.toast.error(
                    f"You must wait {abs(wait_time)} second(s) to submit a message."
                )

        except Exception as e:
            logger.error(e)
            yield rx.toast.error(e)

    def event_state_recover_password(self, recover_dict: dict) -> Iterable[Callable]:
        """
        Recovers password via password recovery page. User must wait 1 min between submissions.
        """
        try:
            current_time = int(time.time())
            wait_interval = 120
            wait_time = (
                int(current_time - wait_interval) - self.user_recovery_email_time
            )
            email = recover_dict.get("email")

            # Check that wait interval isn't sooner than 1 min.
            if wait_time >= 0:
                if email:
                    yield supabase_recover_password(email)
                    yield rx.redirect(
                        "/login/forgot-password/confirmation", replace=True
                    )
                    self.user_recovery_email_time = current_time
                else:
                    raise Exception("Enter a valid email address")

            else:
                yield rx.toast.error(
                    f"You must wait {abs(wait_time)} second(s) to make another recovery attempt."
                )

        except Exception as e:
            logger.error(e)
            yield rx.toast.error(e)

    def redirect_user_to_onboard_or_dashboard(self) -> Iterable[Callable]:
        """
        Used after login to push user to be onboarded, or to the dashboard.
        """
        if self.user_has_reported:
            logger.debug("Sending user to dashboard.")
            yield rx.redirect("/dashboard")
        else:
            logger.debug("Sending user to onboard.")
            yield rx.redirect("/onboard")
