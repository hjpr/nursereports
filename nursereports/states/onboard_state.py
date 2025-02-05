from .user_state import UserState

from typing import Callable, Iterable

import reflex as rx


class OnboardState(UserState):
    has_review: str
    license: str
    license_state: str

    def set_license(self, license: str) -> None:
        self.license = license
        self.license_state = ""
        self.has_review = ""
        if license == "Nursing Student":
            self.has_review = "No"

    def event_state_onboard_flow(self) -> Callable:
        return rx.redirect("/dashboard") if not self.user_needs_onboarding else None

    def event_state_submit_onboard(self) -> Iterable[Callable]:
        try:
            # Check if required fields complete.
            if not (self.license and self.license_state and self.has_review):
                return rx.toast.error("Please complete all required fields.")

            # Update remote database with onboard data.
            user_info = {
                "professional": {
                    "license_type": self.license,
                    "license_state": self.license_state,
                    "license_number": "01234567890"
                },
                "account": {
                    "status": "onboard" if self.has_review == "Yes" else "active"
                }
            }
            self.update_user_info_and_sync_locally(user_info)

            # Decide if user either needs to submit report, or is okay to proceed.
            if self.user_needs_onboarding:
                yield rx.redirect("/search/hospital")
            else:
                yield rx.redirect("/dashboard")

            self.user_is_loading = False

        except Exception as e:
            self.user_is_loading = False
            return rx.toast.error(str(e), close_button=True)
