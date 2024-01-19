
from ..components.custom import spacer
from ..states.report import ReportState

import reflex as rx

def progress_bar() -> rx.Component:
    return rx.box(
        rx.progress(
            value=ReportState.progress,
            color_scheme='teal'
        ),
        spacer(height='4px'),
        rx.text(
            f"{ReportState.progress}%",
            text_align='center'
            ),
        width='100%',
    )