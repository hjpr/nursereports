
from ...states.report_state import ReportState

import reflex as rx

def progress() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(
                        ReportState.comp_progress
                    ),
                    value=ReportState.comp_progress
                ),
                rx.heading(
                    "Compensation",
                    text_decoration=rx.cond(
                        ReportState.comp_is_active, "underline", ""
                        ),
                    size='3'
                ),
                flex_direction='column',
                align_items='center',
                justify_content='center',
                width='30%'
            ),
            rx.spacer(),
            rx.flex(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(
                        ReportState.assign_progress
                    ),
                    value=ReportState.assign_progress
                ),
                rx.heading(
                    "Assignment",
                    text_decoration=rx.cond(
                        ReportState.assign_is_active, "underline", ""
                        ),
                    size='3'
                ),
                flex_direction='column',
                align_items='center',
                justify_content='center',
                width='30%'
            ),
            rx.spacer(),
            rx.flex(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(
                        ReportState.staffing_progress
                    ),
                    value=ReportState.staffing_progress
                ),
                rx.heading(
                    "Staffing",
                    text_decoration=rx.cond(
                        ReportState.staffing_is_active, "underline", ""
                        ),
                    size='3'
                ),
                flex_direction='column',
                align_items='center',
                justify_content='center',
                width='30%'
            ),
            flex_direction='row',
            width='100%'
        ),
        z_index='2',
        background='white',
        border_radius='5px',
        box_shadow='0px 0px 10px 10px white',
        padding_y='12px',
        position='sticky',
        top=['60px', '72px', '72px', '72px', '72px'],
        width='100%'
    )