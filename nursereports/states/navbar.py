
from ..server.supabase.auth import (
    supabase_login_with_email,
    supabase_create_account_with_email
)
from ..server.supabase.feedback import supabase_submit_feedback
from ..states.base import BaseState

from typing import Callable, Iterable

import reflex as rx

class NavbarState(BaseState):
    show_feedback: bool = False
    show_login: bool = False
    login_tab: str = 'login'
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
        self.login_tab = 'login'
        self.show_login = True

    def event_state_toggle_login(self) -> None:
        self.show_login = not self.show_login
        self.error_sign_in_message = None
        self.error_create_account_message = None
    
    def event_state_submit_feedback(self, form_data: dict) -> None:
        """Event to trigger submission of feedback."""
        if form_data['feedback']:
            data = {
                "user_feedback": f"{form_data['feedback']}",
                "email": self.claims['email'],
                "user_id": self.claims['sub']
            }
            response = supabase_submit_feedback(
                self.access_token,
                data
            )
            if response['success']:
                self.show_feedback = False
                self.alert_message = "Thanks for your feedback!"
            else:
                self.error_feedback_message = response['status']

    def event_state_c2a_main(self) -> None:
        self.login_tab = 'create_account'
        self.show_login = True

    def event_state_login_modal_submit(self, form_data: dict) -> Callable | None:
        if form_data.get("login_email"):
            redirect = self.event_state_login_with_email(form_data)
            return redirect
        if form_data.get("create_account_email"):
            self.event_state_email_create_account(form_data)

    def event_state_login_with_email(self, form_data: dict) -> Callable | None:
        email = form_data.get("login_email")
        password = form_data.get("login_password")
        response = supabase_login_with_email(email, password)
        if response['success']:
            self.access_token = response['payload']['access_token']
            self.refresh_token = response['payload']['refresh_token']
            self.show_login = False
            return rx.redirect('/dashboard')
        else:
            self.error_sign_in_message = response['status']

    def event_state_email_create_account(self, form_data: dict) -> None:
        email = form_data.get("create_account_email")
        password = form_data.get("create_account_password")
        password_confirm = form_data.get("create_account_password_confirm")
        if password != password_confirm:
            self.error_create_account_message = "Passwords do not match."
        else:
            response = supabase_create_account_with_email(
                email,
                password
            )
            if response['success']:
                self.show_login = False
                self.error_create_account_message = ""
                self.alert_message = """Email sent with verification
                    link. Allow a few minutes if email doesn't appear
                    right away."""
            else:
                self.error_create_account_message = response['status']
    
    def event_state_logout(self) -> Iterable[Callable]:
        yield rx.redirect("/")
        if self.access_token:
            self.access_token = ""
        if self.refresh_token:
            self.refresh_token = ""
        self.alert_message = "Successfully logged out."