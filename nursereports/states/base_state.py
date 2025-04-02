from ..server.supabase import supabase_update_last_login
from ..states.user_state import UserState
from typing import Callable, Iterable

import reflex as rx
import traceback


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

    def event_state_handle_sso_redirect(self) -> Iterable[Callable]:
        """Checks if there are tokens in url to pull into state."""
        try:
            url = self.router.page.raw_path

            # If user coming from a redirect url containing access and refresh tokens.
            if ("access_token" in url) and ("refresh_token" in url):
                # Format is wonky, just assume this is right. Trust me bro.
                fragment = url.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]

                # For active monthly users purpose.
                supabase_update_last_login(self.access_token, self.user_claims_id)

                # We have to retrieve all our user info.
                self.get_user_info()

                # Send user to appropriate part of site.
                yield self.redirect_user_to_location()

        except Exception:
            traceback.print_exc()
            return rx.toast.error("Error handling SSO redirect.")

    def event_state_requires_login(self) -> Callable:
        """Requires user to be logged in or redirects back to index."""
        try:
            if not self.user_is_authenticated:
                return rx.redirect("/")

        except Exception:
            traceback.print_exc()
            return rx.redirect("/")

    def event_state_requires_report(self) -> Callable:
        """Requires user to be logged in and have intial report submitted."""
        try:
            if self.user_needs_onboarding:
                return rx.redirect("/onboard")

            if not self.user_is_authenticated:
                return rx.redirect("/")

        except Exception:
            traceback.print_exc()
            return rx.redirect("/")
