
from .auth.auth import AuthState

from .pages.auth import AuthAPI
from .pages.deauth import DeauthAPI
from .pages.dashboard import dashboard
from .pages.report import report
from .pages.index import index


from .style.style import style_dict

import reflex as rx


"""
STYLE SHEET - Alter sitewide styles on the stylesheet contained at '/assets'.
"""
style = style_dict
stylesheets = [
    "/stylesheet.css"
]

# INITIALIZE THE APP
app = rx.App(
    style=style,
    stylesheets=stylesheets,
    )

# ADD PAGES HERE
"""
INDEX PAGE - on_load runs login_flow to check states to determine if user is
already logged in, or is coming from an api auth/deauth request.
"""
app.add_page(
    index,
    route="/",
    on_load=AuthState.login_flow
    )

"""
AUTH - pseudo endpoint for SSO redirects. Captures url and parses it
out to get access and refresh tokens as well as redirecting back to root site
allowing for seamless login flow.
"""
app.add_page(
    AuthAPI.page,
    route=AuthAPI.route,
    on_load=AuthState.url_handler,
    )

"""
DEAUTH - pseudo endpoint for SSO redirects. Captures url and parses it out
to remove user data per request of user.
"""
app.add_page(
    DeauthAPI.page,
    route=DeauthAPI.route,
    on_load=AuthState.url_handler,
    )

"""
DASHBOARD - Account panel after signin where user can edit/modify account info
see reports, save hospitals etc.
"""
app.add_page(
    dashboard,
    route="/dashboard",
)

"""
REPORT - Entry page for user report by hospital.
"""
app.add_page(
    report,
    route="/report",
)


# ADD API ROUTES TO BACKEND

# COMPILE TO RUN SERVER
app.compile()
