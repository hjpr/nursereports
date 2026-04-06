from ..states.user_state import UserState
from datetime import datetime, timezone
from typing import Callable, Iterable

import reflex as rx
import traceback


class BaseState(UserState):

    @rx.var
    def host_address(self) -> str:
        """Current domain, ex https://nursereports.org, or http://localhost:3000"""
        return self.router.url.origin

    @rx.var
    def current_location(self) -> str:
        """Current path, ex. /dashboard, or /search/hospital"""
        current_location = self.router.url.path
        return current_location

    def event_state_refresh_login(self) -> Callable | None:
        """Runs on_load prior to every page that may need login information."""
        try:
            if self.user_claims_authenticated and not self.user_claims_expired:
                if (
                    self.user_claims_expiring
                    and self.access_token
                    and self.refresh_token
                ):
                    self.refresh_access_token()
                else:
                    return None
            if self.user_claims_authenticated and self.user_claims_expired:
                self.restore_page_after_login = self.router.page.full_raw_path
                self.access_token = ""
                self.refresh_token = ""
                return rx.redirect("/login")

        except Exception:
            traceback.print_exc()
            return rx.toast.error("Error refreshing tokens.")

    def event_state_check_expired_login(self) -> Callable | None:
        try:
            if self.restore_page_after_login:
                return rx.toast.error("Session expired. Please login again.")
            else:
                return None
        except Exception:
            traceback.print_exc()

    def event_state_handle_sso_redirect(self) -> Iterable[Callable]:
        """Checks if there are tokens in url to pull into state."""
        try:
            url = self.router.url

            if ("access_token" in url) and ("refresh_token" in url):
                fragment = url.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]

                self.query().table("users").eq("id", self.user_claims_id).update(
                    {"last_login": str(datetime.now(timezone.utc).isoformat(timespec="seconds"))},
                    return_="minimal"
                ).execute()

                self.get_user_info()
                yield self.redirect_user_to_location()

        except Exception:
            traceback.print_exc()
            return rx.toast.error("Error handling SSO redirect.")

    def event_state_requires_login(self) -> Callable:
        """Requires user to be logged in or redirects back to index."""
        try:
            if not self.user_claims_authenticated:
                return rx.redirect("/")

        except Exception:
            traceback.print_exc()
            return rx.redirect("/")

    def event_state_requires_report(self) -> Callable:
        """Requires user to be logged in and have intial report submitted."""
        try:
            if self.user_needs_onboarding:
                return rx.redirect("/onboard")

            if not self.user_claims_authenticated:
                return rx.redirect("/")

        except Exception:
            traceback.print_exc()
            return rx.redirect("/")
