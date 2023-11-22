
from ..state.base import State
from typing import Generator, Literal

import httpx
import json
import jwt
import os
import reflex as rx

from dotenv import load_dotenv
load_dotenv()

api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")


class AuthState(State):
    """
    User data returned via JWT from Supabase API call. API endpoints for
    Supabase auth - https://github.com/supabase/gotrue
    """
    # JWT token stored as cookie. Pass to Supabase as header with requests.
    access_token: str = rx.Cookie(
        same_site='strict',
        secure=True,
    )

    # Refresh token stored as cookie for new session request.
    refresh_token: str = rx.Cookie(
        same_site='strict',
        secure=True,
    )

    # Stored url value to extract tokens from.
    url: str = ""

    @rx.cached_var
    def token_is_valid(self) -> bool:
        try:
            jwt.decode(
                self.access_token,
                jwt_key,
                audience='authenticated',
                algorithms=['HS256'],
            )
            return True
        except jwt.ExpiredSignatureError:
            self.get_new_access_token
            try:
                jwt.decode(
                    self.access_token,
                    jwt_key,
                    audience='authenticated',
                    algorithms=['HS256'],
                )
                return True
            except Exception as e:
                print(f"Attempted to refresh expired token.\
                      Retrieved token invalid - {e}")
                return False
        except Exception as e:
            print(f"Token invalid - {e}")
            return False

    @rx.cached_var
    def token_claims(self) -> dict[str, str]:
        try:
            claims = jwt.decode(
                self.access_token,
                jwt_key,
                audience='authenticated',
                algorithms=['HS256'],
            )
            return json.dumps(claims)
        except jwt.ExpiredSignatureError:
            self.get_new_access_token
            try:
                claims = jwt.decode(
                    self.access_token,
                    jwt_key,
                    audience='authenticated',
                    algorithms=['HS256'],
                )
                return json.dumps(claims)
            except Exception as e:
                print(f"Attempted to refresh expired token.\
                      Failed to get claims - {e}")
                return {}
        except Exception as e:
            print(f"Can't get claims - {e}.")
            return {}

    def set_url(self, url):
        """Setter for event handler from url_handler."""
        self.url = url

    def url_handler(self):
        """
        Sets self.url from href when /auth page is loaded, and sets method
        so that we know we're trying to auth with url.
        """
        yield rx.call_script(
            'window.location.href',
            callback=AuthState.set_url
        )
        yield rx.redirect('/')

    def login_flow(self):
        """
        From '/'. Check if url was set by SSO redirect.
        """
        if self.token_is_valid:
            yield rx.redirect('/dashboard')

        if "api/v1/auth" in self.url:
            try:
                fragment = self.url.split('#')[1]
                self.access_token = fragment.split('&')[0].split('=')[1]
                self.refresh_token = fragment.split('&')[4].split('=')[1]
            except Exception as e:
                yield rx.console_log(f"Unexpected URL format passed at '/login'.")
        else:
            yield rx.console_log('Unsupported URL login flow method.')


    def get_new_access_token(self):
        """
        Refresh stored AuthState token. Called if token found to be expired
        when checking from get_claims.
        """
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

        try:
            response = httpx.post(
                url=url,
                params=params,
                headers=headers,
                data=json.dumps(data)
            )
        except Exception as e:
            print(f"{e}")
        
        self.access_token = response.json().get('access_token')
        self.refresh_token = response.json().get('refresh_token')

    async def email_sign_in(self, form_data: dict) -> Generator:
        """
        Takes form_data as dict and submits to Supabase API to get an
        access and refresh token. Returns events to the event handler
        as a generator to set cookies for use on the frontend, change
        active UI elements, and redirect properly.
        """
        from ..components.navbar import NavbarState

        # While working, spin progress circle.
        yield NavbarState.set_sign_in_working(True)

        async with httpx.AsyncClient() as client:

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

            response = await client.post(
                url=url,
                params=params,
                headers=headers,
                data=json.dumps(data),
            )

            if response.is_success:
                # Ensure the JWT that we get is valid and signed by Supabase!
                try:
                    claims = jwt.decode(
                        response.cookies.get('sb-access-token'),
                        jwt_key,
                        audience='authenticated',
                        algorithms=['HS256'],
                    )

                # If invalid, set UI elements for error.
                except Exception as e:
                    yield NavbarState.set_show_error_sign_in(True)
                    yield NavbarState.set_show_error_sign_in_message(
                        response.text.get("error_description")
                    )
                    yield NavbarState.set_sign_in_working(False)

                # Set cookies and values from claims of returned response.
                self.access_token = response.cookies.get('sb-access-token')
                self.refresh_token = response.cookies.get('sb-refresh-token')

                # Set UI elements and redirect.
                yield NavbarState.set_show_sign_in(False)
                yield rx.redirect('/dashboard')

            else:
                # Clear cookies.
                self.access_token = ""
                self.refresh_token = ""

                # Set UI elements for error.
                yield NavbarState.set_show_error_sign_in(True)
                yield NavbarState.set_error_sign_in_message(
                    "Invalid credentials provided."
                )
                yield NavbarState.set_sign_in_working(False)

    async def email_create_account(self, form_data: dict) -> Generator:
        """
        Takes form data from on_submit as dict and submits to Supabase API. Whether
        user signup is successful or not it returns a user in order to prevent db
        introspection. Yields to event handler as generator to set active ui
        elements.
        """
        from ..components.navbar import NavbarState

        # While creating account, spin progress circle.
        yield NavbarState.set_create_account_working(True)

        # Get data from on_submit event via form_data dict.
        email = form_data.get("create_account_email")
        password = form_data.get("create_account_password")
        password_confirm = form_data.get("create_account_password_confirm")

        # Check passwords for match. Supabase enforces 8 character length.
        if password != password_confirm:
            yield NavbarState.set_show_error_create_account(True)
            yield NavbarState.set_error_create_account_message(
                "Passwords do not match."
            )
            yield NavbarState.set_create_account_working(False)

        # If password is ok, continue on to request.
        else:
            async with httpx.AsyncClient() as client:

                # Set up API request.
                url = f'{api_url}/auth/v1/signup'
                headers = {
                    "apikey": api_key,
                    "Content-Type": "application/json",
                    }
                data = {
                    "email": email,
                    "password": password,
                }

                # Make API request.
                response = await client.post(
                    url=url,
                    headers=headers,
                    data=json.dumps(data),
                )

                if response.is_success:
                    # Close our sign in modal and show success message in alert modal.
                    yield NavbarState.set_show_sign_in(False)
                    yield NavbarState.set_show_alert(True)
                    yield NavbarState.set_create_account_working(False)
                    yield NavbarState.set_alert_message(
                        "Sign up successful! Email sent with verification link."
                    )
                
                else:
                    response = response.json()
                    # Make error label visible, set error message.
                    yield NavbarState.set_show_error_create_account(True)
                    yield NavbarState.set_error_create_account_message(
                        response.get('msg')
                    )
                    yield NavbarState.set_create_account_working(False)

    def sso_sign_in(self, provider: str):
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