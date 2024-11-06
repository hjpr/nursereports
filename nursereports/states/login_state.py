
from ..states.base_state import BaseState
from ..server.exceptions import (
    CreateUserFailed,
    DuplicateUserError,
    LoginCredentialsInvalid,
    ReadError,
    RequestFailed,
)
from ..server.secrets import api_url
from ..server.supabase import (
    supabase_create_account_with_email,
    supabase_login_with_email,
)

from loguru import logger
from typing import Callable, Iterable

import reflex as rx

class LoginState(rx.State):
    current_tab: str = "login"
    error_message_login: str = ""
    error_message_create_account: str = ""

    def event_state_submit_login(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the login page.
        """
        try:
            # If user is logging in with email.
            if auth_data.get("login_email"):

                # Grab auth data from form submission.
                email = auth_data.get("login_email")
                password = auth_data.get("login_password")

                # Get JWT using provided auth data.
                tokens = supabase_login_with_email(email, password)
                yield BaseState.set_access_token(tokens.get("access_token"))

                # Refresh user data and send to proper page.
                self.reset()
                yield BaseState.refresh_user_info
                yield BaseState.redirect_user_to_onboard_or_dashboard

            # If user is creating a new account.
            if auth_data.get("create_account_email"):

                # Grab auth data from form submission.
                email = auth_data.get("create_account_email")
                password = auth_data.get("create_account_password")
                password_confirm = auth_data.get("create_account_password_confirm")

                # Check if passwords match
                if password != password_confirm:
                    raise LoginCredentialsInvalid("Passwords do not match")
                
                # Create account from auth data.
                supabase_create_account_with_email(email, password)

                # Reset variables and redirect to the link confirmation page.
                self.reset()
                yield rx.redirect("/login/confirm")

        except Exception as e:
            logger.critical(e)
            self.error_message = e

    def event_state_login_with_sso(self, provider: str) -> Iterable[Callable]:
        """
        Navigate to Supabase SSO endpoint.
        """
        return rx.redirect(f"{api_url}/auth/v1/authorize?provider={provider}")