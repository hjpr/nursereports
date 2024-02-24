
from ..states.report import ReportState

import reflex as rx

def progress() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(ReportState.comp_progress),
                    value=ReportState.comp_progress
                ),
                rx.heading(
                    "Compensation",
                    text_decoration=rx.cond(ReportState.comp_is_active, "underline", "")
                    ),
                width='30%'
            ),
            rx.spacer(),
            rx.vstack(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(ReportState.assign_progress),
                    value=ReportState.assign_progress
                ),
                rx.heading(
                    "Assignment",
                    text_decoration=rx.cond(ReportState.assign_is_active, "underline", "")
                    ),
                width='30%'
            ),
            rx.spacer(),
            rx.vstack(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(ReportState.staffing_progress),
                    value=ReportState.staffing_progress
                ),
                rx.heading(
                    "Staffing",
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
        width='100%'
    )