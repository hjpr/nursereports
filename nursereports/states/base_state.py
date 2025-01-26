from ..states.user_state import UserState

from loguru import logger
from typing import Callable, Iterable

import reflex as rx
import urllib



class BaseState(UserState):

    @rx.var
    def host_address(self) -> str:
        """
        Current domain, ex "https://nursereports.org, or http://localhost:3000"
        """
        return self.router.page.host
    
    @rx.var
    def current_location(self) -> str:
        """
        Current path, ex. "/dashboard, or /search/hospital"
        """
        current_location = self.router.page.path
        return current_location

    def event_state_auth_flow(self) -> Iterable[Callable]:
        """
        Simple standard login flow. Runs on_load prior to every page.
        """
        try:
            # If user is coming from a redirect.
            if "#" in self.current_location:
                parsed_url = urllib.parse(self.current_location)
                logger.debug(f"Parsed url - {parsed_url}")

            # If user is authenticated.
            if self.user_claims_authenticated:
                # Ensure expiring access tokens are refreshed.
                if self.user_claims_expiring and (self.access_token and self.refresh_token):
                    self.refresh_access_token()

                # Ensure user data is present and current.
                if not (self.user_info and self.local_user_data_synced_with_remote()):
                    self.get_user_info()

            # If user is not authenticated.
            if not self.user_claims_authenticated:
                # User claims are expired
                if self.access_token or self.refresh_token:
                    self.clear_tokens()
                    yield rx.redirect("/")

                # User coming from an SSO redirect.
                url = self.router.page.raw_path
                if ("access_token" in url) and ("refresh_token" in url):
                    yield from self.set_tokens()

        except Exception as e:
            logger.critical(e)
            yield rx.toast.error("Failed authentication checks.")
            yield rx.redirect("/")

    def event_state_access_flow(self, required_status: str) -> Iterable[Callable]:
        """
        Restricts page access based on page requirements. Pass "login" to require
        user to be logged in, or pass "report" to require user to have submitted
        a report.
        """
        try:
            if required_status == "login" and not self.user_claims_authenticated:
                yield rx.redirect("/")
                yield rx.toast.error("Please login to access that page.")

            if required_status == "report" and self.user_needs_onboarding:
                yield rx.redirect("/onboard")
                yield rx.toast.error("Please submit a report to access that page.")

        except Exception as e:
            logger.critical(e)
            yield rx.toast.error("Failed access checks.")
            yield rx.redirect("/")
