
from ..states.navbar import NavbarState
from ..states.report import ReportState

import reflex as rx

def progress() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.circular_progress(
                    rx.circular_progress_label(ReportState.comp_progress),
                    value=ReportState.comp_progress
                ),
                rx.heading(
                    "Compensation", size='xs',
                    text_decoration=rx.cond(ReportState.comp_is_active, "underline", "")
                    ),
                width='30%'
            ),
            rx.spacer(),
            rx.vstack(
                rx.circular_progress(
                    rx.circular_progress_label(ReportState.assign_progress),
                    value=ReportState.assign_progress
                ),
                rx.heading(
                    "Assignment", size='xs',
                    text_decoration=rx.cond(ReportState.assign_is_active, "underline", "")
                    ),
                width='30%'
            ),
            rx.spacer(),
            rx.vstack(
                rx.circular_progress(
                    rx.circular_progress_label(ReportState.staffing_progress),
                    value=ReportState.staffing_progress
                ),
                rx.heading(
                    "Staffing", size='xs',
                    text_decoration=rx.cond(ReportState.staffing_is_active, "underline", "")
                    ),
                width='30%'
            ),
            width='100%'
        ),
        z_index='2',
        background='white',
        border_radius='5px',
        box_shadow='0px 0px 10px 10px white',
        padding_y='20px',
        position='sticky',
        top=rx.cond(NavbarState.show_c2a, '100px', '60px'),
        width='100%'
    )