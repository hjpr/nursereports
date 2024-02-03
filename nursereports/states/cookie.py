
from loguru import logger
from typing import Callable, Iterable

import httpx
import json
import jwt
import os
import reflex as rx
import rich
import time

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")

class CookieState(rx.State):
    """
    CookieState inherits the base state, so any other states that
    need access should inherit from CookieState. They can then 
    access cookies via self.access_token or self.refresh_token.
    """
    # JWT token stored as cookie. Pass to Supabase as header with requests.
    access_token: str = rx.Cookie(
        name="access_token",
        same_site='strict',
        #domain='nursereports.org',
        secure=True,
    )

    # Refresh token stored as cookie for new session request.
    refresh_token: str = rx.Cookie(
        name="refresh_token",
        same_site='strict',
        #domain='nursereports.org',
        secure=True,
    )

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
        
    @rx.cached_var
    def user_is_authenticated(self) -> bool:
        """
        If claims returned as dict, then claims present, else a str
        is returned with an error status.
        """
        if isinstance(self.claims, dict):
            logger.debug("User is authenticated.")
            return True
        if isinstance(self.claims, str):
            logger.warning("User is not authenticated.")
            return False
        
    @rx.cached_var
    def user_has_reported(self) -> bool:
        """
        User metadata contains has_reported, which determines what
        areas of site user can access when logged in.
        """
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

    def get_new_access_token(self) -> Iterable[Callable]:
        """
        Gets a new access token using the refresh token stored in cookies.
        If successful, yields events to set new cookies, if unsuccessful, 
        yields a redirect back to '/'.
        """
        from ..states.navbar import NavbarState

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
            yield CookieState.set_access_token(response.json().get('access_token'))
            yield CookieState.set_refresh_token(response.json().get('refresh_token'))
        else:
            logger.critical("Unable to retrieve new access token.")
            yield rx.redirect('/')
            yield NavbarState.set_alert_message(
                "Failed to refresh session. Please sign in again."
            )

    def standard_flow(self, access_level) -> Iterable[Callable] | None:
            """
            Check claims and access to determine if redirect is necessary.
            If pages require a special flow, then use standard_flow as
            a template and add additional checks.
            """
            yield from self.check_claims()
            yield from self.check_access(access_level)

    def check_claims(self) -> Iterable[Callable] | None:
        from ..states.navbar import NavbarState

        logger.debug("Checking claims...")

        if isinstance(self.claims, dict):
            """
            Refresh token if user active from 30 min -> 5 sec prior
            to expiration. Otherwise let expire and force user to 
            relogin for inactivity.
            """
            current_time = int(time.time())
            expires_at = self.claims['exp']
            time_left_sec = (expires_at - current_time)
            if 5 <= time_left_sec <= 1800:
                logger.warning(f"Within claims expiration window. Timeleft - {time_left_sec}")
                yield CookieState.get_new_access_token
        elif isinstance(self.claims, str):
            """
            If str returned, then claims have already expired, so
            allow redirect via check_access and set appropriate
            alert message here.
            """
            if self.claims == 'expired':
                yield NavbarState.set_alert_message(
                    "For your security you've been logged out for inactivity."
                )
            if self.claims == 'invalid':
                yield NavbarState.set_alert_message(
                    "Access token corrupted. Login to refresh."
                )
        else:
            logger.debug("Somethin fucky goin on...")
            rich.inspect(self.claims)

    def check_access(self, access_level) -> Iterable[Callable] | None:
        """
        Uses string to determine what level of access is required to
        visit the page.
        """
        if access_level == 'req_none':
            # Use req_none to grant open access to any page.
            yield None
        if access_level == 'req_login' and not self.user_is_authenticated:
            # Use req_login to require user to login.
            yield rx.redirect('/')
        if access_level == 'req_report' and not self.user_has_reported:
            # Use req_report to force users to submit report before access.
            yield rx.redirect('/search/report')