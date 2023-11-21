
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
    _url: str = ""
    _url_method: Literal['auth' , 'deauth'] = ""

    def set_url_from_script(self, url):
        """Setter for event handler from url_handler func."""
        self._url = url

    def set_url_method(self, url_method):
        self._url_method = url_method

    def auth_handler(self):
        """
        Sets self.url from href when /auth page is loaded, and sets method
        so that we know we're trying to auth with _url.
        """
        yield rx.call_script(
            'window.location.href',
            callback=AuthState.set_url_from_script
        )
        yield AuthState.set_url_method('auth')
        yield rx.redirect('/')

    def deauth_handler(self):
        """
        Sets self.url from href when /deauth page is loaded, and sets method
        so that we know we're trying to deauth with _url.
        """
        yield rx.call_script(
            'window.location.href',
            callback=AuthState.set_url_from_script
        )
        yield AuthState.set_url_method('deauth')
        yield rx.redirect('/')

    async def login_flow(self):
        """
        1. Check if _url and _url_method were set by SSO redirect. ->
        2. Process _url as specified in _url_method. ->
        3. Check if access and refresh token were set from prior login/SSO redirect->
        4. Validate claims from token to ensure they are valid ->
        5. Profit ->
        """
        if self._url and self._url_method:
            if self._url_method == 'auth':
                try:
                    fragment = self._url.split('#')[1]
                    self.access_token = fragment.split('&')[0].split('=')[1]
                    self.refresh_token = fragment.split('&')[4].split('=')[1]
                except Exception as e:
                    yield rx.console_log(f"Unexpected URL format passed at '/login'.")
            elif self._url_method == 'deauth':
                # Figure out what to pass to remove user info from database.
                pass
            else:
                yield rx.console_log('Unsupported URL login flow method.')

        if self.access_token and self.refresh_token:
            async for item in self.authenticate_token():
                yield item

    async def authenticate_token(self):
        """
        Authenticate JWT access token as signed by Supabase.

        If claims expired, then _get_claims will attempt to use refresh token
        to make API request for new access token.
        """
        from ..components.navbar import NavbarState

        claims = await self._get_claims()
        if isinstance(claims, dict):
            self._url = ''
            self._url_method = ''
            yield NavbarState.set_is_authenticated(True)
            yield rx.redirect('/dashboard')
        else:
            self.access_token=''
            self.refresh_token=''
            self._url = ''
            yield NavbarState.set_is_authenticated(False)
            yield rx.console_log("Invalid token present as cookie.")

    async def _get_claims(self) -> dict | bool:
        """
        Get claims from access_token JWT. Will raise exception if JWT signature
        isn't correct, or has expired. Either returns False or returns the
        claims as a dict.
        """
        try:
            claims = await jwt.decode(
                self.access_token,
                jwt_key,
                audience='authenticated',
                algorithms=['HS256'],
            )
            return claims
        
        except jwt.ExpiredSignatureError:
            if await self._get_new_access_token():
                claims = await jwt.decode(
                    self.access_token,
                    jwt_key,
                    audience='authenticated',
                    algorithms=['HS256'],
                )
                return claims
            else:
                rx.console_log(f"Token expired - unable to renew.")
                return False

        # Catch other reasons token is invalid.    
        except Exception as e:
            rx.console_log(f"Getting claims failed - {e}")
            return False
    
    async def _get_new_access_token(self):
        """
        Refresh stored AuthState token. Called if token found to be expired
        when checking from _get_claims.
        """
        async with httpx.AsyncClient() as client:
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
                response = await client.post(
                    url=url,
                    params=params,
                    headers=headers,
                    data=json.dumps(data)
                    )
            except Exception as e:
                return False
            
            # Convert response object to json and extract tokens.
            f_response = response.json()
            self.access_token = f_response.get('access_token')
            self.refresh_token = f_response.get('refresh_token')
            return True

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

            # Set up our API request.
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

            # Make our request.
            response = await client.post(
                url=url,
                params=params,
                headers=headers,
                data=json.dumps(data),
            )

            if response.is_success:
                # Grab our tokens from set-cookies in Response object.
                access_token = response.cookies.get('sb-access-token')
                refresh_token = response.cookies.get('sb-refresh-token')

                # Ensure the JWT that we get is valid and signed by Supabase!
                try:
                    claims = jwt.decode(
                        access_token,
                        jwt_key,
                        audience='authenticated',
                        algorithms=['HS256'],
                    )

                # If invalid, set error message and stop spinning progress circle.
                except Exception as e:
                    yield NavbarState.set_show_error_sign_in(True)
                    yield NavbarState.set_show_error_sign_in_message(
                        response.text.get("error_description")
                    )
                    yield NavbarState.set_sign_in_working(False)

                # Set cookies and values from claims of returned response.
                email = claims.get('email')
                self.access_token = access_token
                self.refresh_token = refresh_token
                yield NavbarState.set_email(email)

                # Set NavbarState as logged in, and close login window.
                yield NavbarState.set_show_sign_in(False)
                yield NavbarState.set_is_authenticated(True)

                # Redirect to dashboard, uncomment and utilize below to add...
                yield rx.redirect('/dashboard')

            else:
                # Clear cookies.
                self.access_token = ""
                self.refresh_token = ""

                # Make error label visible, set error message.
                yield NavbarState.set_show_error_sign_in(True)
                yield NavbarState.set_error_sign_in_message(
                    "Invalid credentials provided."
                )

                # Stop spinning progress circle.
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