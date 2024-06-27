from ..server.exceptions import (
    CreateUserError,
    DuplicateUserError,
    LoginAttemptError,
    ReadError,
    RequestError,
)
from ..server.secrets import api_url
from ..server.supabase import (
    supabase_create_account_with_email,
    supabase_login_with_email,
    supabase_submit_feedback,
)
from .base_state import BaseState

from typing import Callable, Iterable

import reflex as rx


class NavbarState(BaseState):
    show_feedback: bool = False
    show_login: bool = False
    login_tab: str = "login"
    alert_message: str
    error_sign_in_message: str
    error_create_account_message: str
    error_feedback_message: str

    @rx.var
    def show_alert_message(self) -> bool:
        return True if self.alert_message else False

    def set_show_feedback(self, feedback) -> None:
        self.error_feedback_message = ""
        self.show_feedback = feedback

    def event_state_navbar_pressed_sign_in(self) -> None:
        self.login_tab = "login"
        self.show_login = True

    def event_state_toggle_login(self) -> None:
        self.show_login = not self.show_login
        self.error_sign_in_message = None
        self.error_create_account_message = None

    def event_state_submit_feedback(self, form_data: dict) -> None:
        """Event to trigger submission of feedback."""
        if form_data["feedback"]:
            data = {
                "user_feedback": f"{form_data['feedback']}",
                "email": self.user_claims["payload"]["email"],
                "user_id": self.user_claims["payload"]["sub"],
            }
            response = supabase_submit_feedback(self.access_token, data)
            if response["success"]:
                self.show_feedback = False
                self.alert_message = "Thanks for your feedback!"
            else:
                self.error_feedback_message = response["status"]

    def event_state_c2a_main(self) -> None:
        self.login_tab = "create_account"
        self.show_login = True

    def event_state_login_modal_submit(self, form_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the login_modal. Gets form_data from the event and
        can either login using email or create an account with an email.
        """
        try:
            if form_data.get("login_email"):
                self.login_with_email(form_data)
            if form_data.get("create_account_email"):
                self.email_create_account(form_data)
        except CreateUserError as e:
            error_message = str(e)
            self.error_create_account_message = error_message
        except LoginAttemptError as e:
            error_message = str(e)
            self.error_sign_in_message = error_message
        except (DuplicateUserError, ReadError, RequestError) as e:
            error_message = str(e)
            yield rx.toast.error(error_message, timeout=5000)
            yield rx.redirect("/logout/error")

    def login_with_email(
        self, form_data: dict
    ) -> Iterable[Callable] | None:
        """
        Logs into supabase using email and password in order and saves the access_token
        and refresh_token to the state.
        """
        email = form_data.get("login_email")
        password = form_data.get("login_password")
        tokens = supabase_login_with_email(email, password)
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.show_login = False
        self.error_sign_in_message = ""
        self.set_all_user_data()
        self.redirect_user_to_onboard_or_dashboard()

    def email_create_account(self, form_data: dict) -> None:
        email = form_data.get("create_account_email")
        password = form_data.get("create_account_password")
        password_confirm = form_data.get("create_account_password_confirm")
        if password != password_confirm:
            raise LoginAttemptError("Passwords do not match")
        supabase_create_account_with_email(email, password)
        self.show_login = False
        self.error_create_account_message = ""
        self.alert_message = """Email sent with verification
            link. Allow a few minutes if email doesn't appear
            right away."""

    def event_state_login_with_sso(self, provider: str) -> Callable:
        self.show_login = False
        return rx.redirect(f"{api_url}/auth/v1/authorize?provider={provider}")
