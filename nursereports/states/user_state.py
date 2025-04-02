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
    supabase_update_last_login
)
from suplex import Suplex

from datetime import datetime, timezone
from rich.console import Console
from typing import Callable, Iterable

import copy
import humanize
import math
import rich
import reflex as rx
import time
import traceback

console = Console()


class UserState(Suplex):

    MAX_HOSPITALS_DISPLAYED = 5
    MAX_REPORTS_DISPLAYED = 5

    # If user login expires during state event, save url here.
    restore_page_after_login: str = ""

    # Used to display loading wheel for user UI events.
    user_is_loading: bool = False

    # Stored dicts of user information.
    user_info: dict[str, str | list | dict | None] = {}
    user_reports: list[dict[str, str]] = []
    user_saved_hospitals: list[dict[str, str]] = []
    current_hospital_page: int = 1
    current_report_page: int = 1

    # User rate limits.
    user_contact_email_time: int = 0
    user_recovery_email_time: int = 0
    
    @rx.var
    def user_info_specialties(self) -> list:
        return self.user_info.get("professional", {}).get("specialty", [])
    
    @rx.var
    def user_info_license_type(self) -> str:
        return self.user_info.get("professional", {}).get("license_type", "")
    
    @rx.var
    def user_info_license_state(self) -> str:
        return self.user_info.get("professional", {}).get("license_state", "")
    
    @rx.var
    def user_info_experience(self) -> int:
        return self.user_info.get("professional", {}).get("experience", 0)
    
    @rx.var(cache=True)
    def user_needs_onboarding(self) -> bool:
        if self.user_info:
            return True if self.user_info.get("account").get("status") == "onboard" else False
        else:
            return True
        
    @rx.var()
    def paginated_saved_hospitals(self) -> list[dict]:
        if len(self.user_saved_hospitals) > self.MAX_HOSPITALS_DISPLAYED:
            # Determine number of pages.
            num_pages = math.ceil(len(self.user_saved_hospitals) / self.MAX_HOSPITALS_DISPLAYED)
            num_pages_list = [ page for page in range(1, num_pages + 1) ]

            # Build dict.
            paginated_hospitals = { number: [] for number in num_pages_list } 

            # Fill dict.
            current_page = 1
            for hospital in self.user_saved_hospitals:
                if len(paginated_hospitals[current_page]) >= self.MAX_HOSPITALS_DISPLAYED:
                    current_page += 1
                paginated_hospitals[current_page].append(hospital)
            
            return paginated_hospitals.get(self.current_hospital_page)
        
        else:
            return self.user_saved_hospitals
        
    @rx.var()
    def paginated_user_reports(self) -> list[dict]:
        """
        Paginates the list of dicts and returns the associated page. Also sorts so that
        more recent reports are shown first.
        """
        if len(self.user_reports) > self.MAX_REPORTS_DISPLAYED:
            # Determine number of pages.
            num_pages = math.ceil(len(self.user_reports) / self.MAX_REPORTS_DISPLAYED)
            num_pages_list = [ page for page in range(1, num_pages + 1) ]

            # Build dict.
            paginated_reports = { number: [] for number in num_pages_list }

            # Sort by date.
            sorted_reports = sorted(self.user_reports, key=lambda report: report["modified_at"] or report["created_at"], reverse=True)

            # Fill dict.
            current_page = 1
            for report in sorted_reports:
                if len(paginated_reports[current_page]) >= self.MAX_REPORTS_DISPLAYED:
                    current_page += 1
                paginated_reports[current_page].append(report)

            return paginated_reports.get(self.current_report_page)
        
        else:
            return sorted(self.user_reports, key=lambda report: report["modified_at"] or report["created_at"], reverse=True)

    @rx.var
    def num_hospital_pages(self) -> int:
        return math.ceil(len(self.user_saved_hospitals) / self.MAX_HOSPITALS_DISPLAYED)
    
    @rx.var
    def num_report_pages(self) -> int:
        return math.ceil(len(self.user_reports) / self.MAX_REPORTS_DISPLAYED)
    
    def next_hospital_page(self) -> None:
        num_pages = math.ceil(len(self.user_saved_hospitals) / self.MAX_HOSPITALS_DISPLAYED)
        if self.current_hospital_page < num_pages:
            self.current_hospital_page += 1
    
    def previous_hospital_page(self) -> None:
        if self.current_hospital_page > 1:
            self.current_hospital_page -= 1

    def next_report_page(self) -> None:
        num_pages = math.ceil(len(self.user_reports) / self.MAX_REPORTS_DISPLAYED)
        if self.current_report_page < num_pages:
            self.current_report_page += 1

    def previous_report_page(self) -> None:
        if self.current_report_page > 1:
            self.current_report_page -= 1


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
            console.print_exception(show_locals=True)
            yield rx.toast.error(str(e), close_button=True)
            self.user_is_loading = False

    def event_state_login_with_sso(self, provider: str) -> Iterable[Callable]:
        """
        Navigate to Supabase SSO endpoint.
        """
        try:
            # Supabase API endpoint for SSO auth.
            yield rx.redirect(f"{api_url}/auth/v1/authorize?provider={provider}")

        except Exception as e:
            console.print_exception(show_locals=True)
            yield rx.toast.error(
                str(e),
                close_button=True,
            )
            self.user_is_loading = False

    def get_user_info(self) -> None:
        """
        Get user info or create entry in /users table if user info missing (1st login)
        """
        # Get user info or create entry in /users
        user_info = self.query.table("users").select("*").eq("id", self.user_id).execute()
        if user_info:
            self.user_info = user_info[0]
        else:
            user_info = {
                "id": self.user_id,
                "modified_at": None,
                "last_login": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                "account": {
                    "created_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                    "status": "onboard",
                    "trust": 0,
                    "membership": "free",
                    "browsers": []
                },
                "professional": {
                    "license_type": "",
                    "license_number": "",
                    "license_state": "",
                    "specialty": [],
                    "experience": 0
                },
                "reports": {
                    "ids": [],
                    "num_full": 0,
                    "num_flag": 0,
                    "num_pay": 0
                },
                "engagement": {
                    "likes": 0,
                    "tags": 0,
                    "referrals": []
                },
                "preferences": {
                    "email": "",
                    "mobile": "",
                    "dark_mode": False,
                    "status_opt_in": False,
                    "update_opt_in": False,
                    "social_opt_in": False,
                },
                "saved": {
                    "jobs": [],
                    "hospitals": []
                }
            }
            self.query.table("users").upsert(user_info).execute()

    def get_user_hospital_info(self) -> None:
        """
        If user has saved hospital, populate info with hospital details.
        """
        saved_hospital_list = self.user_info.get("saved", {}).get("hospitals", [])
        complete_hospital_info = []

        if saved_hospital_list:
            complete_hospital_info = self.query.table("hospitals").select(
                "hosp_name,hosp_state,hosp_city,hosp_id,hosp_addr"
            ).in_("hosp_id", saved_hospital_list).execute()

            for hospital in complete_hospital_info:
                hospital["hosp_city"] = hospital["hosp_city"].title()
                hospital["hosp_addr"] = hospital["hosp_addr"].title()
        
        self.user_saved_hospitals = complete_hospital_info

    def get_user_reports(self) -> None:
        """
        Get all user reports.
        """
        reports = self.query.table("reports").select(
            "report_id,hospital_id,assignment,hospital,created_at,modified_at"
            ).eq("user_id", self.user_id).execute()
        if reports:
            for report in reports:
                # Format from nested -> top-level for access via rx.foreach
                report["area"] = report["assignment"]["area"]["selected_area"] + report["assignment"]["area"]["entered_area"]
                report["unit"] = report["assignment"]["unit"]["selected_unit"] + report["assignment"]["unit"]["entered_unit"]
                report["role"] = report["assignment"]["role"]["selected_role"] + report["assignment"]["role"]["entered_role"]
                report["hospital_city"] = report["hospital"]["city"].title()
                report["hospital_state"] = report["hospital"]["state"]

                # Format timestamps
                report["time_ago"] = humanize.naturaltime(datetime.fromisoformat(report["created_at"]))
                if report["modified_at"]:
                    report["time_ago"] = humanize.naturaltime(datetime.fromisoformat(report["modified_at"])) 
        
        self.user_reports = reports

    def update_user_info_and_sync_locally(
        self, 
        data: dict[str, any]
    ) -> Iterable[Callable]:
        """
        Provide user info data to update to remote database, then save to local state.
        Updates nested JSONB fields by sending the complete parent object.
        """
        data_to_sync = {}
        user_info = copy.deepcopy(self.user_info)

        # Recursively update dicts down the tree.
        def update(original: dict, new: dict):
            for key, value in new.items():
                if isinstance(value, dict):
                    original[key] = update(original.get(key, {}), value)
                else:
                    original[key] = value
            return original

        update(user_info, data)

        # Compare at the top-level so we can send the entire column if change occurred.
        local_user_info = copy.deepcopy(self.user_info)
        for key in data:
            if user_info[key] != local_user_info[key]:
                data_to_sync[key] = user_info[key]

        if data_to_sync:
            synced_data = supabase_update_user_info(
                self.access_token, 
                self.user_claims_id, 
                data_to_sync
            )
            self.user_info.update(synced_data)

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
            if len(self.user_info["saved"]["hospitals"]) >= 30:
                return rx.toast.error("Maximum number of saved hospitals reached. (30)")

            # Check for duplicates.
            if hosp_id in self.user_info["saved"]["hospitals"]:
                return rx.toast.error("Hospital is already in saved hospitals.", close_button=True)

            # Add to list.
            data = {
                "saved": {
                    "hospitals": self.user_info["saved"]["hospitals"] + [hosp_id]
                }
            }
            self.update_user_info_and_sync_locally(data)
            yield rx.toast.success("Hospital added to 'Saved Hospitals'.", close_button=True)

        except RequestFailed as e:
            yield rx.toast.error(str(e), close_buttons=True)
        except Exception as e:
            traceback.print_exc()
            logger.critical(str(e))
            yield rx.toast.error("Unable to save hospital to list.", close_button=True)

    def event_state_remove_hospital(self, hosp_id: str) -> Iterable[Callable]:
        """
        Removes a selected hospital from user's saved hospital list.
        """
        try:
            # Make a new list not including selected hospital.
            updated_hospitals = [
                h for h in self.user_info["saved"]["hospitals"] if h != hosp_id
            ]

            # Sent to database and update local info.
            data = {
                "saved": {
                    "hospitals": updated_hospitals
                }
            }
            self.update_user_info_and_sync_locally(data)
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

    def redirect_user_to_location(self) -> Callable:
        """
        Used after login to push user to be onboarded, dashboard, or restores the page
        they were on when login expired.
        """
        if self.restore_page_after_login:
            logger.debug(f"Sending user back to {self.restore_page_after_login}")
            return rx.redirect(self.restore_page_after_login)
        if self.user_needs_onboarding:
            logger.debug(f"Sending {self.user_claims_id} to onboard.")
            return rx.redirect("/onboard")
        else:
            logger.debug(f"Sending {self.user_claims_id} to dashboard.")
            return rx.redirect("/dashboard")
