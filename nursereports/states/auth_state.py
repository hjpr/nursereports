
from httpx import HTTPStatusError
from rich.console import Console
from .user_state import UserState
from typing import Callable, Iterable

import reflex as rx
import time

console = Console()


class AuthState(UserState):

    recovery_email_timeout: int

    def login_with_password(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the login page. Retrieves necessary user info.
        """
        try:
            yield AuthState.setvar("is_loading", True)
            if auth_data.get("email") and auth_data.get("password"):
                email = auth_data.get("email")
                password = auth_data.get("password")
                self.sign_in_with_password(email=email, password=password)
                yield UserState.get_user_info()
                yield UserState.get_user_hospital_info()
                yield UserState.get_user_reports()
                yield rx.redirect("/")
            else:
                yield rx.toast.error("Both fields are required.")
            yield AuthState.setvar("is_loading", False)

        except HTTPStatusError as e:
            yield rx.toast.error(e.response.json()["msg"])
            yield AuthState.setvar("is_loading", False)
        except Exception:
            console.print_exception(show_locals=True)
            yield rx.toast.error("Login failed.")
            yield AuthState.setvar("is_loading", False)

    def login_with_sso(self, provider: str) -> Iterable[Callable]:
        """
        Navigate to Supabase SSO endpoint. On action, user will be sent to callback url.
        """
        try:
            yield AuthState.setvar("is_loading", True)
            redirect_url = AuthState.sign_in_with_oauth(provider=provider)
            yield rx.redirect(redirect_url)
            yield AuthState.setvar("is_loading", False)

        except HTTPStatusError as e:
            yield rx.toast.error(e.response.json()["msg"])
            yield AuthState.setvar("is_loading", False)
        except Exception as e:
            console.print_exception(show_locals=True)
            yield rx.toast.error(str(e), close_button=True)
            yield AuthState.setvar("is_loading", False)

    def create_account(self, auth_data: dict) -> Iterable[Callable]:
        """
        Handles the on_submit event from the create-account page.
        """
        try:
            yield AuthState.setvar("is_loading", True)
            email = auth_data.get("create_account_email")
            password = auth_data.get("create_account_password")
            password_confirm = auth_data.get("create_account_password_confirm")
            if password != password_confirm:
                raise ValueError("Passwords do not match.")
            
            self.sign_up(email=email, password=password)
            yield rx.redirect("/login/confirm")
            yield AuthState.setvar("is_loading", False)

        except HTTPStatusError as e:
            yield rx.toast.error(e.response.json()["msg"])
            yield AuthState.setvar("is_loading", False)
        except Exception as e:
            console.print_exception(show_locals=True)
            yield rx.toast.error(str(e), close_button=True)
            yield AuthState.setvar("is_loading", False)

    def recover_password(self, recover_dict: dict) -> Iterable[Callable]:
        """
        Recovers password via password recovery page. User must wait 1 min between submissions.
        """
        try:
            yield AuthState.setvar("is_loading", True)
            yield
            email = recover_dict.get("email")
            if not email:
                raise ValueError("Enter email address to recover.")

            current_time = int(time.time())
            wait_interval = 120
            wait_time = (
                int(current_time - wait_interval) - AuthState.get_var_value("recovery_email_timeout")
            )
            if wait_time >= 0:
                self.reset_password_email(email=email)
                yield rx.redirect(
                    "/login/forgot-password/confirmation", replace=True
                )
                self.recovery_email_timeout = current_time
            else:
                yield rx.toast.error(
                    f"You must wait {abs(wait_time)} second(s) to make another recovery attempt."
                )
            yield AuthState.setvar("is_loading", False)

        except HTTPStatusError as e:
            yield rx.toast.error(e.response.json()["msg"])
            yield AuthState.setvar("is_loading", False)
        except Exception as e:
            console.print_exception(show_locals=True)
            yield rx.toast.error(e)  
            yield AuthState.setvar("is_loading", False)    

    def logout(self) -> Iterable[Callable] | None:
        try:
            yield AuthState.setvar("is_loading", True)
            self.log_out()
            yield rx.redirect("/")
            yield AuthState.setvar("is_loading", False)

        except HTTPStatusError as e:
            yield rx.toast.error(e.response.json()["msg"])
            yield AuthState.setvar("is_loading", False)  
        except Exception as e:
            console.print_exception(show_locals=True)
            yield rx.toast.error(str(e))
            yield AuthState.setvar("is_loading", False)