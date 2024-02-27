
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.report import ReportState

import reflex as rx

@rx.page(
    route="/report/summary/[summary_id]",
    title='Nurse Reports',
    on_load=BaseState.event_state_standard_flow('login')
)
@login_protected
def summary_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        rx.flex(
            rx.center(
                rx.vstack(
                    rx.cond(
                        rx.State.is_hydrated,
                        rx.cond(
                            ReportState.hosp_info,
                            rx.vstack(
                                rx.heading(
                                    "You are submitting a report for...",
                                    text_align='center'
                                ),
                                rx.heading(
                                    f"{ReportState.hosp_info['hosp_name']}",
                                    text_align='center'
                                ),
                                rx.heading(
                                    f"{ReportState.hosp_info['hosp_addr']}, "\
                                    f"{ReportState.hosp_info['hosp_state']} "\
                                    f"{ReportState.hosp_info['hosp_zip']}",
                                    text_align='center'
                                )
                            )
                        ),
                        rx.chakra.spinner()
                    ),
                    spacer(height='40px'),
                    rx.vstack(
                        rx.flex(
                            rx.hstack(
                                rx.image(
                                    src='/raster/anonymous.png',
                                    height='100px',
                                    width='100px'
                                ),
                                rx.center(
                                    rx.text("""Reports are anonymous. No
                                        personal information will be displayed
                                        on your report.
                                        """,
                                        padding_x='20px'
                                    ),
                                    width='100%'
                                )
                            ),
                            width='100%'
                        ),
                        rx.divider(),
                        rx.flex(
                            rx.hstack(
                                rx.image(
                                    src='/raster/people-talking.png',
                                    height='100px',
                                    width='100px'
                                ),
                                rx.center(
                                    rx.text("""Our report database is built to
                                        only benefit nurses. We are not
                                        affiliated with hospitals or other
                                        business interests.
                                        """,
                                        padding_x='20px'
                                    ),
                                )
                            ),
                            width='100%'
                        ),
                        rx.divider(),
                        rx.flex(
                            rx.hstack(
                                rx.image(
                                    src='/raster/time.png',
                                    height='100px',
                                    width='100px'
                                ),
                                rx.center(
                                    rx.text("""We value your time. Submitting your
                                            report will only take you about 4-7
                                            minutes.
                                            """,
                                            padding_x='20px'
                                            ),
                                    width='100%'
                                ),
                            ),
                            width='100%'
                        ),
                        width='100%'
                    ),
                    spacer(height='40px'),
                    rx.button(
                        "Got it. Let's go!",
                        on_click=ReportState.clear_and_nav_to_compensation,
                    ),
                    width='600px'
                )
            ),
            padding_x='20px',
            width=['100%', '100%', '600px', '600px', '600px'],
            max_width='1200px',
            flex_direction='column',
            flex_basis='auto',
            flex_grow='1',
            flex_shrink='0',
        ),
        spacer(height='80px'),
        footer(),
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )