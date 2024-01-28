
from ..states.cookie import CookieState
from loguru import logger
from typing import Callable, Iterable

import httpx
import json
import os
import reflex as rx

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")

class AuthState(CookieState):
    """
    User data returned via JWT from Supabase API call. API endpoints for
    Supabase auth - https://github.com/supabase/gotrue
    """

    def email_sign_in(self, form_data: dict) -> Iterable[Callable]:
        """
        Takes form_data as dict and submits to Supabase API to get an
        access and refresh token. Returns events to the event handler
        as a generator to set cookies for use on the frontend, change
        active UI elements, and redirect properly.
        """
        from ..states.navbar import NavbarState

        url = f'{api_url}/auth/v1/token'
        params = {
            "grant_type": "password",
        }
        headers = {
            "apikey": api_key,
            "Content-Type": "application/json",
        }
        data = {
            "email": form_data.get("sign_in_email"),
            "password": form_data.get("sign_in_password"),
        }
        response = httpx.post(
            url=url,
            params=params,
            headers=headers,
            data=json.dumps(data),
        )

        if response.is_success:
            yield CookieState.set_access_token(response.cookies.get('sb-access-token'))
            yield CookieState.set_refresh_token(response.cookies.get('sb-refresh-token'))
            yield NavbarState.set_show_sign_in(False)
            yield rx.redirect('/dashboard')
        else:
            yield NavbarState.set_error_sign_in_message(
                "Invalid credentials provided."
            )

    def email_create_account(self, form_data: dict) -> Iterable[Callable]:
        """
        Takes form data from on_submit as dict and submits to Supabase API. Whether
        user signup is successful or not it returns a user in order to prevent db
        introspection. Yields to event handler as generator to set active ui
        elements.
        """
        from ..states.navbar import NavbarState

        email = form_data.get("create_account_email")
        password = form_data.get("create_account_password")
        password_confirm = form_data.get("create_account_password_confirm")

        # Supabase enforces 8 character length.
        if password != password_confirm:
            yield NavbarState.set_error_create_account_message(
                "Passwords do not match."
            )
        else:
            url = f'{api_url}/auth/v1/signup'
            headers = {
                "apikey": api_key,
                "Content-Type": "application/json",
                }
            data = {
                "email": email,
                "password": password,
            }

            response = httpx.post(
                url=url,
                headers=headers,
                data=json.dumps(data),
            )

            if response.is_success:
                yield NavbarState.set_show_sign_in(False)
                yield NavbarState.set_error_create_account_message("")
                yield NavbarState.set_alert_message(
                    "Sign up successful! Email sent with verification link."
                )
            else:
                response = response.json()
                yield NavbarState.set_error_create_account_message(
                    response.get('msg')
                )

    def sso_sign_in(self, provider: str) -> Iterable[Callable]:
        """
        Takes positional str which determines the SSO provider to send
        request to. Redirection chain ends up at the '/v1/auth/'
        pseudoendpoint.
        """
        from ..states.navbar import NavbarState
        
        yield NavbarState.set_show_sign_in(False)
        yield rx.redirect(
            f"{api_url}/auth/v1/authorize?provider={provider}",
            )
        
    def logout(self) -> Iterable[Callable]:
        """
        Clears cookies and redirects back to root.
        """
        from ..states.navbar import NavbarState

        yield rx.redirect("/")
        yield rx.remove_cookie("access_token")
        yield rx.remove_cookie("refresh_token")
        yield NavbarState.set_alert_message("Successfully logged out.")

    # def initial_setup(self) -> Iterable[Event]:
    #     """
    #     Creating user via email or SSO is different, so func runs to
    #     ensure that user_metadata contains the proper fields for the
    #     site flow. Namely helps us to know if user has submitted a 
    #     report, what membership they have, and their trust level.

    #     Membership:
    #     "NR" = Hasn't submitted a report yet.
    #     "F" = Free tier.
    #     "P" = Paid tier.
        
    #     """
    #     url = f'{api_url}/auth/v1/user'
    #     headers = {
    #         "apikey": api_key,
    #         "Authorization" : f"Bearer {AuthState.access_token}",
    #         "Content-Type": "application/json",
    #         }
    #     data = {
    #         "data": {
    #             "membership": "NR"
    #             }
    #     }
    #     async with httpx.AsyncClient() as client:
    #         response = client.put(
    #             url=url,
    #             headers=headers,
    #             data=json.dumps(data),
    #         )

    #         if response.is_success:
    #             logger.debug("Added user fields. Refreshing token.")
    #             self.get_new_access_token()