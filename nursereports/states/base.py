
from ..events.auth import event_supabase_get_new_access_token

import jwt
import os
import reflex as rx
import rich
import time

from dotenv import load_dotenv
from loguru import logger
from typing import Callable, Iterable

load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")

class BaseState(rx.State):

    access_token: str = rx.Cookie(
        name="access_token",
        same_site='strict',
        secure=True,
    )

    refresh_token: str = rx.Cookie(
        name="refresh_token",
        same_site='strict',
        secure=True,
    )

    @rx.cached_var
    def claims(self) -> dict[str, str] | str:
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
            logger.critical(f"Can't retrieve claims - {e}")
            return "other"
        
    @rx.cached_var
    def user_is_authenticated(self) -> bool:
        if isinstance(self.claims, dict):
            if self.claims['aud'] == 'authenticated':
                logger.debug("User is authenticated.")
                return True
            else:
                return False
        if isinstance(self.claims, str):
            logger.warning("User is not authenticated.")
            return False
        
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

    def get_new_access_token(self) -> Iterable:
        response = event_supabase_get_new_access_token(
            self.access_token,
            self.refresh_token
            )
        if response["success"]:
            self.access_token = response["payload"]["access_token"]
            self.refresh_token = response["payload"]["refresh_token"]
        else:
            yield rx.redirect('/')

    def check_claims(self) -> Iterable | None:
        from ..states.navbar import NavbarState
        if isinstance(self.claims, dict):
            current_time = int(time.time())
            expires_at = self.claims['exp']
            time_left_sec = (expires_at - current_time)
            if 5 <= time_left_sec <= 1800:
                self.get_new_access_token()
        else:
            if self.claims == 'expired':
                yield NavbarState.set_alert_message(
                    "For security you've been logged out for inactivity."
                )

    def check_access(self, access_level) -> Iterable | None:
        if access_level == 'req_none':
            yield None
        if access_level == 'req_login' and not self.user_is_authenticated:
            yield rx.redirect('/')
        if access_level == 'req_report' and not self.user_has_reported:
            yield rx.redirect('/onboard')

    def standard_flow(self, access_level) -> Iterable[Callable] | None:
        yield from self.check_claims()
        yield from self.check_access(access_level)