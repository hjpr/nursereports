
from .middleware.middleware import LoggingMiddleware

from .pages.api_auth import auth_api
from .pages.api_deauth import deauth_api
from .pages.dashboard import dashboard
from .pages.index import index
from .pages.report_summary import summary
from .pages.report_pay import pay_page
from .pages.report_staffing import staffing_page
from .pages.report_assign import assign_page
from .pages.report_complete import complete
from .pages.search import search

from .states.cookie import CookieState
from .style.style import style_dict

import reflex as rx

"""
STYLE SHEET - Alter sitewide styles on the stylesheet contained
at '/assets'.
"""
style = style_dict
stylesheets = [
    "/stylesheet.css"
]

# INITIALIZE THE APP
app = rx.App(
    # style=style,
    # stylesheets=stylesheets,
    middleware=[LoggingMiddleware()]
    )

# ADD PAGES HERE
"""
INDEX PAGE - on_load runs login_flow to check states to determine
if user is already logged in, or is coming from an api auth/deauth
request.
"""
app.add_page(
    index,
    route="/",
    on_load=CookieState.standard_flow('req_none'),
    )

"""
AUTH - pseudo endpoint for SSO redirects. Captures url and parses
it out to get access and refresh tokens as well as redirecting back
to root site allowing for seamless login flow.
"""
app.add_page(
    auth_api,
    route="api/v1/auth",
    on_load=CookieState.standard_flow('req_none')
    )

"""
DEAUTH - pseudo endpoint for SSO redirects. Captures url and parses
it out to remove user data per request of user.
"""
app.add_page(
    deauth_api,
    route="/api/v1/deauth",
    on_load=CookieState.standard_flow('req_login')
    )

"""
DASHBOARD - Account panel after signin where user can edit/modify
account info see reports, save hospitals etc.
"""
app.add_page(
    dashboard,
    route="/dashboard",
    on_load=CookieState.standard_flow('req_report')
)

"""
SEARCH- Search by hospital which routes to proper page depending on
the context of the search. For example, page is used both to search
hospitals to submit a report, but also to search hospitals to access
hospital page.
"""
app.add_page(
    search,
    route="/search/[context]",
    on_load=CookieState.standard_flow('req_login')
)

#####################################################################
#
# REPORT PAGES
# 
#####################################################################

"""
REPORT SUMMARY - Entry page for user report by hospital.
"""
app.add_page(
    summary,
    route="/report/summary/[summary_id]",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT PAY - Pay report by hospital
"""
app.add_page(
    pay_page,
    route="/report/submit/[report_id]/compensation",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT STAFFING- Staffing report by hospital.
"""
app.add_page(
    staffing_page,
    route="/report/submit/[report_id]/staffing",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT UNIT - Unit report by hospital.
"""
app.add_page(
    assign_page(),
    route="/report/submit/[report_id]/assignment",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT COMPLETE - Unit report by hospital.
"""
app.add_page(
    complete,
    route="/report/submit/[report_id]/complete",
    on_load=CookieState.standard_flow('req_login')
)