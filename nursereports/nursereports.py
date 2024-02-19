
from .middleware.middleware import LoggingMiddleware

from .pages.dashboard import dashboard
from .pages.index import index
from .pages.onboard import onboard_page
from .pages.report_summary import summary_page
from .pages.report_summary_comp import comp_summary_page
from .pages.report_comp import comp_page
from .pages.report_summary_assign import assign_summary_page
from .pages.report_assign import assign_page
from .pages.report_summary_staffing import staffing_summary_page
from .pages.report_staffing import staffing_page
from .pages.report_complete import complete
from .pages.search import search
from .pages.sso import sso_page

from .states.auth import AuthState
from .states.cookie import CookieState

import reflex as rx

# INITIALIZE THE APP
app = rx.App(
    middleware=[LoggingMiddleware()],
    theme=rx.theme(accent_color='teal')
)

#####################################################################
#
# API
#
#####################################################################

"""
SSO Endpoint
"""
app.add_page(
    sso_page,
    route="/api/auth/[params]",
    on_load=AuthState.parse_auth
)

#####################################################################
#
# INDEX
#
#####################################################################

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

#####################################################################
#
# DASHBOARDS - REQ REPORTS
#
#####################################################################

"""
MAIN DASHBOARD - Account panel after signin where user can edit/modify
account info see reports, save hospitals etc.
"""
app.add_page(
    dashboard,
    route="/dashboard",
    on_load=CookieState.standard_flow('req_report')
)

#####################################################################
#
# SEARCH PAGES - REQ LOGIN/REPORT DEPENDING
#
#####################################################################

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
# ONBOARDING - REQ LOGIN
#
#####################################################################

app.add_page(
    onboard_page,
    route='/onboard',
    on_load=CookieState.standard_flow('req_login')
)

#####################################################################
#
# REPORT PAGES - REQ LOGIN
# 
#####################################################################

"""
REPORT SUMMARY - Entry page for user report by hospital.
"""
app.add_page(
    summary_page,
    route="/report/summary/[summary_id]",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT COMPENSATION SUMMARY - Description of compensation.
"""
app.add_page(
    comp_summary_page,
    route="/report/submit/[report_id]/compensation/summary",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT COMPENSATION - Pay/benefits report by hospital
"""
app.add_page(
    comp_page,
    route="/report/submit/[report_id]/compensation",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT ASSIGNMENT SUMMARY - Description of assignment.
"""
app.add_page(
    assign_summary_page,
    route="/report/submit/[report_id]/assignment/summary",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT ASSIGNMENT - Assignment report by hospital.
"""
app.add_page(
    assign_page,
    route="/report/submit/[report_id]/assignment",
    on_load=CookieState.standard_flow('req_login')
)
"""
REPORT STAFFING SUMMARY - Description of staffing.
"""
app.add_page(
    staffing_summary_page,
    route="/report/submit/[report_id]/staffing/summary",
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
REPORT COMPLETE - Unit report by hospital.
"""
app.add_page(
    complete,
    route="/report/submit/[report_id]/complete",
    on_load=CookieState.standard_flow('req_login')
)