
from ..components.footer import footer
from ..components.progress_bar import progress_bar
from ..components.navbar import navbar, c2a_spacer
from ..components.lists import cities_by_state
from ..components.custom import spacer
from ..states.report import ReportState

import reflex as rx

def summary() -> rx.Component:
    return rx.flex(

        navbar(),

        c2a_spacer(),

        progress_bar(),

        spacer(height='40px'),

        # MAIN CONTENT CONTAINER
        rx.flex(
            rx.center(
                rx.vstack(
                    rx.cond(
                        rx.State.is_hydrated,
                        # STATE HYDRATED TRUE
                        rx.cond(
                            ReportState.hosp_info,
                            # HOSP INFO TRUE
                            rx.vstack(
                                rx.heading(
                                    "You are submitting a report for...",
                                    size='md',
                                    text_align='center'
                                ),
                                rx.heading(
                                    f"{ReportState.hosp_info['hosp_name']}",
                                    size='md',
                                    text_align='center'
                                ),
                                rx.heading(
                                    f"{ReportState.hosp_info['hosp_addr']}, "\
                                    f"{ReportState.hosp_info['hosp_state']} "\
                                    f"{ReportState.hosp_info['hosp_zip']}",
                                    size='md',
                                    text_align='center'
                                )
                            )
                            # HOSP INFO FALSE
                        ),
                        # STATE HYDRATED FALSE
                        rx.spinner()
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


                        # STYLING FOR VSTACK CONTAINING CARDS
                        spacing='1.5em',
                        width='100%'

                    ),
                    spacer(height='40px'),
                    rx.button(
                        "Got it. Let's go!",
                        color_scheme='teal',
                        on_click=ReportState.nav_summary_to_pay,
                        is_loading=~rx.State.is_hydrated,
                    ),
                    width='600px'
                )
            ),

            # STYLING FOR CONTENT CONTAINER
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

        # STYLING FOR BODY CONTAINER
        width='100%',
        flex_direction='column',

        align_items='center',
        min_height='100vh',
    )