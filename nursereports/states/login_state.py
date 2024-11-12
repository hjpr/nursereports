
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
import rich

class LoginState(rx.State):
    error_message_login: str = ""
    error_message_create_account: str = ""

    def event_state_submit_login(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the login page.
        """
        try:
            # Disable login attempts while request is out.
            yield BaseState.set_is_loading(True)

            if auth_data.get("email") and auth_data.get("password"):

                # Grab auth data from form submission.
                email = auth_data.get("email")
                password = auth_data.get("password")

                # Get JWT using provided auth data.
                tokens = supabase_login_with_email(email, password)
                rich.inspect(tokens)
                yield BaseState.set_access_token(tokens.get("access_token"))

                # Send to proper page.
                yield BaseState.redirect_user_to_onboard_or_dashboard

            # If either email or password are missing.
            else:
                yield rx.toast.error("Both fields are required.")

            # Re-enable login attempts after requests.
            yield BaseState.set_is_loading(False)

        except Exception as e:
            logger.warning(e)
            yield rx.toast.error(e)
            yield BaseState.set_is_loading(False)


    def event_state_create_account(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the create-account page.
        """
        try:
            BaseState.set_is_loading(True)

            if (
                auth_data.get("create_account_email") and
                auth_data.get("create_account_password") and
                auth_data.get("create_account_password_confirm")
            ):

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
                yield rx.redirect("/login/confirm")

            else:
                yield rx.toast.error("All fields must be completed.")

            yield BaseState.set_is_loading(False)

        except Exception as e:
            logger.error(e)
            yield rx.toast.error(e, close_button=True, duration=10000)
            yield BaseState.set_is_loading(False)

    def event_state_login_with_sso(self, provider: str) -> Iterable[Callable]:
        """
        Navigate to Supabase SSO endpoint.
        """
        try:
            yield BaseState.set_is_loading(True)
            yield rx.redirect(f"{api_url}/auth/v1/authorize?provider={provider}")
            yield BaseState.set_is_loading(False)
        except Exception as e:
            logger.error(e)
            yield rx.toast.error(e)
            yield BaseState.set_is_loading(False)