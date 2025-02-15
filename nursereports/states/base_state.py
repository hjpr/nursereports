from ..states.user_state import UserState
from typing import Callable

import reflex as rx


class BaseState(UserState):
    @rx.var
    def host_address(self) -> str:
        """Current domain, ex https://nursereports.org, or http://localhost:3000"""
        return self.router.page.host

    @rx.var
    def current_location(self) -> str:
        """Current path, ex. /dashboard, or /search/hospital"""
        current_location = self.router.page.path
        return current_location

    def event_state_refresh_login(self) -> Callable:
        """Runs on_load prior to every page that may need login information."""
        try:
            if self.user_claims_authenticated:
                # Ensure expiring access tokens are refreshed.
                if self.user_claims_expiring and (
                    self.access_token and self.refresh_token
                ):
                    self.refresh_access_token()

        except Exception:
            return rx.toast.error("Error refreshing tokens.")

    def event_state_handle_sso_redirect(self) -> Callable:
        """Checks if there are tokens in url to pull into state."""
        try:
            url = self.router.page.raw_path
            if ("access_token" in url) and ("refresh_token" in url):
                fragment = url.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]
        except Exception:
            return rx.toast.error("Error handling SSO redirect.")

    def event_state_requires_login(self) -> Callable:
        """Requires user to be logged in or redirects back to index."""
        try:
            if not self.user_claims_authenticated:
                return rx.redirect("/")

        except Exception:
            return rx.redirect("/")

    def event_state_requires_report(self) -> Callable:
        """Requires user to be logged in and have intial report submitted."""
        try:
            if self.user_needs_onboarding:
                return rx.redirect("/onboard")

            if not self.user_claims_authenticated:
                return rx.redirect("/")

        except Exception:
            return rx.redirect("/")
