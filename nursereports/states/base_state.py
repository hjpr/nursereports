from datetime import datetime, timezone
from ..states.user_state import UserState
from rich.console import Console
from typing import Callable, Iterable

import reflex as rx

console = Console()


class BaseState(UserState):
    @rx.var
    def host_address(self) -> str:
        """
        Current domain, ex https://nursereports.org, or http://localhost:3000
        """
        return self.router.page.host

    @rx.var
    def current_location(self) -> str:
        """
        Current path, ex. /dashboard, or /search/hospital
        """
        return self.router.page.path

    def event_state_handle_sso_redirect(self) -> Iterable[Callable]:
        """
        Checks if there are tokens in url to pull into state
        """
        try:
            url = self.router.page.raw_path

            if ("access_token" in url) and ("refresh_token" in url):
                # Format is wonky, just assume this is right. Trust me bro.
                fragment = url.split("#")[1]
                self.access_token = fragment.split("&")[0].split("=")[1]
                self.refresh_token = fragment.split("&")[4].split("=")[1]

                # For active monthly users purpose.
                data = {
                    "last_login": str(
                        datetime.now(timezone.utc).isoformat(timespec="seconds")
                    )
                }
                query = (
                    self.query.table("users").update(data=data).eq("id", self.user_id)
                )
                query.execute()  # Already going to get user info, no need to return user data.

                self.get_user_info()

                yield self.redirect_user_to_location()

        except Exception:
            console.print_exception()
            return rx.toast.error("Error handling SSO redirect.")

    def event_state_requires_login(self) -> Callable:
        """Requires user to be logged in or redirects back to index."""
        try:
            if not self.user_is_authenticated:
                return rx.redirect("/")

        except Exception:
            console.print_exception()
            return rx.redirect("/")

    def event_state_requires_report(self) -> Callable:
        """Requires user to be logged in and have intial report submitted."""
        try:
            if self.user_needs_onboarding:
                return rx.redirect("/onboard")

            if not self.user_is_authenticated:
                return rx.redirect("/")

        except Exception:
            console.print_exception()
            return rx.redirect("/")
