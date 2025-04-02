
import reflex as rx
import rich

from httpx import HTTPStatusError
from rich.console import Console
from .user_state import UserState
from typing import Callable, Iterable

console = Console()


class AuthState(UserState):

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

    def logout(self) -> Callable | None:
        try:
            self.log_out()
            return rx.redirect("/")
        except Exception as e:
            return rx.toast.error(str(e))