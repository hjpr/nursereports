
from ..states.report import ReportState

import reflex as rx

def progress() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.circular_progress(
                    rx.circular_progress_label(ReportState.pay_progress),
                    value=ReportState.pay_progress
                ),
                rx.heading("Compensation", size='xs'),
                width='30%'
            ),
            rx.spacer(),
            rx.vstack(
                rx.circular_progress(
                    rx.circular_progress_label(ReportState.staffing_progress),
                    value=ReportState.staffing_progress
                ),
                rx.heading("Staffing", size='xs'),
                width='30%'
            ),
            rx.spacer(),
            rx.vstack(
                rx.circular_progress(
                    rx.circular_progress_label(ReportState.assign_progress),
                    value=ReportState.assign_progress
                ),
                rx.heading("Assignment", size='xs'),
                width='30%'
            ),
            width='100%'
        ),
        width='100%'
    )