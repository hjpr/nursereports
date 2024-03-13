
from ..components.c2a import c2a
from ..components.custom import spacer, login_protected
from ..components.footer import footer
from ..components.navbar import navbar
from ...states.base import BaseState
from ...states.summary import SummaryState

import reflex as rx

@rx.page(
    route="/report/submit/[hosp_id]/summary",
    title='Nurse Reports',
    on_load=[
        BaseState.event_state_standard_flow('login'),
        SummaryState.event_state_get_hospital_info
        ]
)
@login_protected
def summary_page() -> rx.Component:
    return rx.flex(
        c2a(),
        navbar(),
        spacer(height='40px'),
        content(),
        spacer(height='80px'),
        footer(),
        width='100%',
        flex_direction='column',
        align_items='center',
        min_height='100vh',
    )

def content() -> rx.Component:
    return rx.flex(
        hospital_info(),
        hospital_info_error(),
        section_anonymous(),
        section_motivation(),
        section_time(),
        buttons(),
        gap='24px',
        padding_x='20px',
        width=['100%', '500px', '500px', '500px', '500px'],
        flex_direction='column',
        flex_basis='auto',
        flex_grow='1',
        flex_shrink='0',
    )

def hospital_info() -> rx.Component:
    return rx.card(
        rx.cond(
            rx.State.is_hydrated,
            rx.cond(
                SummaryState.hosp_info,
                rx.flex(
                    rx.heading(
                        "You are submitting a report for...",
                        size='4'
                    ),
                    spacer(height='12px'),
                    rx.heading(
                        f"{SummaryState.hosp_info['hosp_name']}",
                        text_align='center'
                    ),
                    rx.heading(
                        f"{SummaryState.hosp_info['hosp_addr']}, "\
                        f"{SummaryState.hosp_info['hosp_state']} "\
                        f"{SummaryState.hosp_info['hosp_zip']}",
                        text_align='center'
                    ),
                    flex_direction='column',
                    gap='4px',
                    align_items='center',
                    justify_content='center',
                    width='100%'
                )
            ),
            rx.flex(
                rx.chakra.spinner(),
                align_items='center',
                justify_content='center'
            )
        ),
        variant='ghost'
    )

def hospital_info_error() -> rx.Component:
    return rx.cond(
        SummaryState.error_hosp_info,
        rx.flex(
            rx.callout(
                f"Unable to retrieve hospital info. {SummaryState.error_hosp_info}",
                icon='alert_triangle',
                color_scheme='red',
                role='alert'
            ),
        )
    )

def section_anonymous() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.hstack(
                rx.image(
                    src='/raster/anonymous.png',
                    height='100px',
                    width='100px'
                ),
                rx.flex(
                    rx.text(
                        """
                        All reporting is anonymous. No personal details
                        are attached to your report.
                        """,
                        padding_x='20px'
                    ),
                    height='100%',
                    width='100%',
                    align_items='center',
                    justify_content='center'
                )
            )
        )
    )

def section_motivation() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.hstack(
                rx.image(
                    src='/raster/people-talking.png',
                    height='100px',
                    width='100px'
                ),
                rx.flex(
                    rx.text(
                        """
                        This database is only for nursing interests.
                        I am not affiliated with hospitals or
                        corporations.
                        """,
                        padding_x='20px'
                    ),
                    height='100%',
                    width='100%',
                    align_items='center',
                    justify_content='center'
                )
            )
        )
    )

def section_time() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.hstack(
                rx.image(
                    src='/raster/time.png',
                    height='100px',
                    width='100px'
                ),
                rx.flex(
                    rx.text(
                        """
                        Your time is valuable. This should only take
                        about 5 minutes. 
                        """,
                        padding_x='20px'
                        ),
                    height='100%',
                    width='100%',
                    align_items='center',
                    justify_content='center'
                )
            )
        )
    )

def buttons() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.button(
                "Got it. Let's go!",
                rx.icon("arrow-big-right"),
                size='3',
                variant='ghost',
                on_click=SummaryState.event_state_goto_report,
            ),
            justify_content='center'
        )
    )