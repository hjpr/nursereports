from ...states.report_state import ReportState
from .tailwind import flex

import reflex as rx


def progress() -> rx.Component:
    return flex(
        rx.flex(
            rx.flex(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(ReportState.comp_progress),
                    value=ReportState.comp_progress,
                ),
                rx.text(
                    "Compensation",
                    text_decoration=rx.cond(
                        ReportState.comp_is_active, "underline", ""
                    ),
                    class_name="text-sm uppercase",
                ),
                class_name="flex-col justify-center items-center space-y-2 w-[30%]"
            ),
            rx.spacer(),
            rx.flex(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(ReportState.assign_progress),
                    value=ReportState.assign_progress,
                ),
                rx.text(
                    "Assignment",
                    text_decoration=rx.cond(ReportState.assign_is_active, "underline", ""),
                    class_name="text-sm uppercase",
                ),
                class_name="flex-col justify-center items-center space-y-2 w-[30%]"
            ),
            rx.spacer(),
            rx.flex(
                rx.chakra.circular_progress(
                    rx.chakra.circular_progress_label(ReportState.staffing_progress),
                    value=ReportState.staffing_progress,
                ),
                rx.text(
                    "Staffing",
                    text_decoration=rx.cond(
                        ReportState.staffing_is_active, "underline", ""
                    ),
                    class_name="text-sm uppercase",
                ),
                class_name="flex-col justify-center items-center space-y-2 w-[30%]"
            ),
            flex_direction="row",
            width="100%",
        ),
        class_name="flex-row z-10 rounded py-3 sticky top-16 w-full"
    )
