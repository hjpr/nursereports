
from .auth.auth import AuthState
from .middleware.middleware import AuthMiddleware
from .pages.api_auth import auth_api
from .pages.api_deauth import deauth_api
from .pages.dashboard import dashboard
from .pages.index import index
from .pages.report import report
from .pages.search import search
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
    middleware=[AuthMiddleware()]
    )

# ADD PAGES HERE
"""
INDEX PAGE - on_load runs login_flow to check states to determine if user is
already logged in, or is coming from an api auth/deauth request.
"""
app.add_page(
    index,
    route="/",
    on_load=AuthState.auth_flow('req_none'),
    )

"""
AUTH - pseudo endpoint for SSO redirects. Captures url and parses it
out to get access and refresh tokens as well as redirecting back to root site
allowing for seamless login flow.
"""
app.add_page(
    auth_api,
    route="api/v1/auth",
    on_load=AuthState.auth_flow('req_none')
    )

"""
DEAUTH - pseudo endpoint for SSO redirects. Captures url and parses it out
to remove user data per request of user.
"""
app.add_page(
    deauth_api,
    route="/api/v1/deauth",
    on_load=AuthState.auth_flow('req_login')
    )

"""
DASHBOARD - Account panel after signin where user can edit/modify account info
see reports, save hospitals etc.
"""
app.add_page(
    dashboard,
    route="/dashboard",
    on_load=AuthState.auth_flow('req_report')
)

"""
SEARCH- Search by hospital which routes to proper page depending on the context
of the search. For example, page is used both to search hospitals to submit a 
report, but also to search hospitals to access hospital page.
"""
app.add_page(
    search,
    route="/search/[context]",
    on_load=AuthState.auth_flow('req_login')
)

"""
REPORT - Entry page for user report by hospital.
"""
app.add_page(
    report,
    route="/report/[hosp_id]",
    on_load=AuthState.auth_flow('req_login')
)
