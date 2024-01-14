
from typing import Iterable
from reflex.event import Event

import httpx
import json
import jwt
import os
import reflex as rx
import rich

from dotenv import load_dotenv
from loguru import logger
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")


class AuthState(rx.State):
    """
    User data returned via JWT from Supabase API call. API endpoints for
    Supabase auth - https://github.com/supabase/gotrue
    """
    # JWT token stored as cookie. Pass to Supabase as header with requests.
    access_token: str = rx.Cookie(
        name="access_token",
        same_site='strict',
        secure=True,
    )

    # Refresh token stored as cookie for new session request.
    refresh_token: str = rx.Cookie(
        name="refresh_token",
        same_site='strict',
        secure=True,
    )

    @rx.cached_var
    def user_has_reported(self) -> bool:
        if isinstance(self.claims, dict):
            if self.claims.get("has_reported"):
                logger.debug("User has submitted the required report.")
                return True
            else:
                logger.warning("User hasn't submitted the required report.")
                return False
        else:
            logger.warning("No claims to pull user report status.")
            return False

    @rx.cached_var
    def user_is_authenticated(self) -> bool:
        if isinstance(self.claims, dict):
            logger.debug("User is authenticated.")
            return True
        if isinstance(self.claims, str):
            logger.warning("User is not authenticated.")
            return False

    @rx.cached_var
    def claims(self) -> dict[str, str] | str:
        """
        Will only return dict of claims if user is authenticated,
        otherwise returns string with error description to match.
        """
        try:
            claims = jwt.decode(
                self.access_token,
                jwt_key,
                audience='authenticated',
                algorithms=['HS256'],
            )
            return claims
        except jwt.ExpiredSignatureError:
            logger.warning("Claims expired!")
            return "expired"
        except jwt.InvalidAudienceError:
            logger.critical("Claims invalid!")
            return "invalid"
        except Exception as e:
            logger.warning(f"Can't retrieve claims - {e}")
            return "other"

    def get_new_access_token(self) -> Iterable[Event]:
        """
        Gets a new access token using the refresh token stored in cookies.
        If successful, yields events to set new cookies, if unsuccessful, 
        yields a redirect back to '/'.
        """
        from ..components.navbar import NavbarState

        logger.debug("Attempting to refresh expired access token...")

        url = f"{api_url}/auth/v1/token"
        params = {
            "grant_type": "refresh_token"
        }
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        data = {
            "refresh_token": self.refresh_token
        }

        response = httpx.post(
            url=url,
            params=params,
            headers=headers,
            data=json.dumps(data)
        )

        if response.is_success:
            logger.debug("Refreshed user access tokens.")
            yield AuthState.set_access_token(response.json().get('access_token'))
            yield AuthState.set_refresh_token(response.json().get('refresh_token'))
            yield NavbarState.set_alert_message("")
        else:
            logger.debug("Unable to retrieve new access token.")
            yield rx.redirect('/')
            yield NavbarState.set_alert_message(
                "Failed to refresh session. Please sign in again."
            )

    def email_sign_in(self, form_data: dict) -> Iterable[Event]:
        """
        Takes form_data as dict and submits to Supabase API to get an
        access and refresh token. Returns events to the event handler
        as a generator to set cookies for use on the frontend, change
        active UI elements, and redirect properly.
        """
        from ..components.navbar import NavbarState

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
            yield AuthState.set_access_token(response.cookies.get('sb-access-token'))
            yield AuthState.set_refresh_token(response.cookies.get('sb-refresh-token'))
            yield NavbarState.set_show_sign_in(False)
            yield rx.call_script(
                "window.location.reload()"
            )
            yield rx.redirect('/dashboard')
        else:
            yield NavbarState.set_error_sign_in_message(
                "Invalid credentials provided."
            )

    def email_create_account(self, form_data: dict) -> Iterable[Event]:
        """
        Takes form data from on_submit as dict and submits to Supabase API. Whether
        user signup is successful or not it returns a user in order to prevent db
        introspection. Yields to event handler as generator to set active ui
        elements.
        """
        from ..components.navbar import NavbarState

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

    def sso_sign_in(self, provider: str) -> Iterable[Event]:
        """
        Takes positional str which determines the SSO provider to send
        request to. Redirection chain ends up at the '/v1/auth/'
        pseudoendpoint.
        """
        from ..components.navbar import NavbarState
        
        yield NavbarState.set_show_sign_in(False)
        yield rx.redirect(
            f"{api_url}/auth/v1/authorize?provider={provider}",
            )
        
    def logout(self) -> Iterable[Event]:
        """
        Clears cookies and redirects back to root.
        """
        from ..components.navbar import NavbarState

        yield rx.redirect("/")
        yield rx.remove_cookie("access_token")
        yield rx.remove_cookie("refresh_token")
        yield NavbarState.set_alert_message("Successfully logged out.")

    def auth_flow(self, access_level) -> Iterable[rx.event.Event]:
        """
        Seamlessly refreshes access tokens mid-navigation if token is
        expired. Also either allows navigation to protected pages, or
        redirects back to root if unauthorized.
        """
        from ..components.navbar import NavbarState

        if isinstance(self.claims, str):
            if self.claims == 'expired':
                yield AuthState.get_new_access_token
            if self.claims == 'invalid':
                yield NavbarState.set_alert_message(
                    "Access token corrupted. Login to refresh."
                )
        if access_level == 'req_none':
            # Use req_none to grant open access to any page.
            pass
        if access_level == 'req_login' and not self.user_is_authenticated:
            # Use req_login to require user to login.
            yield rx.redirect('/')
            yield NavbarState.set_alert_message(
                "Please login to access that page."
            )
        if access_level == 'req_report' and not self.user_has_reported:
            # Use req_report to force users to submit report before access.
            yield rx.redirect('/report/search')
            yield NavbarState.set_alert_message(
                "Please submit your own report in order to access those resources."
            )

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