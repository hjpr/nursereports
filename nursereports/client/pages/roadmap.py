from ..components import navbar, footer, flex, text
import reflex as rx


@rx.page(
    route="/roadmap", title="Nurse Reports"
)
def roadmap_page() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        footer(),
        class_name="flex-col items-center dark:bg-zinc-900 min-h-svh w-full",
    )


def content() -> rx.Component:
    return rx.flex(
        rx.flex(
            header(),
            image(),
            class_name="flex-col-reverse md:flex-col gap-10 md:gap-12 w-full max-w-[700px]",
        ),
        map(),
        class_name="flex-col grow items-center px-8 py-16 md:pt-24 md:pb-48 space-y-12 md:space-y-16 w-full max-w-screen-lg",
    )


def header() -> rx.Component:
    return rx.flex(
        text("Roadmap", class_name="text-4xl font-bold"),
        class_name="flex-col items-start md:items-center text-lg w-full",
    )

def image() -> rx.Component:
    return rx.flex(
        flex(
            text("PLACEHOLDER", class_name="text-xs"),
            class_name="flex-col items-center justify-center rounded-lg border bg-white aspect-video w-full max-w-[700px]",
        ),
        class_name="flex-col items-center w-full",
    )

def map() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("goal", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Soft Launch", class_name="text-lg font-bold"),
                    text("February 2025", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle-check-big", class_name="stroke-green-400 dark:stroke-teal-600"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                text("Non public launch for refinement and feature testing.",),
                class_name="p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        rx.flex(
            rx.flex(
                class_name="h-8 md:h-16 w-[1px] bg-zinc-200 dark:bg-zinc-700"
            ),
            class_name="flex items-center justify-center w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("target", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Hard Launch", class_name="text-lg font-bold"),
                    text("May 2025", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle", class_name="stroke-zinc-200 dark:stroke-zinc-700"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                text("Public launch with basic features, and grassroots social media campaign."),
                class_name="p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        rx.flex(
            rx.flex(
                class_name="h-8 md:h-16 w-[1px] bg-zinc-200 dark:bg-zinc-700"
            ),
            class_name="flex items-center justify-center w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("target", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Refine UI/UX", class_name="text-lg font-bold"),
                    text("May 2025 - July 2025", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle", class_name="stroke-zinc-200 dark:stroke-zinc-700"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                text("Refine user experience via user feedback after hard launch."),
                text("Research user requested features to be added in Major Feature Release #2."),
                class_name="flex-col p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        rx.flex(
            rx.flex(
                class_name="h-8 md:h-16 w-[1px] bg-zinc-200 dark:bg-zinc-700"
            ),
            class_name="flex items-center justify-center w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("target", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Major Feature Release #1", class_name="text-lg font-bold"),
                    text("August 2025", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle", class_name="stroke-zinc-200 dark:stroke-zinc-700"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                rx.flex(
                    text("Hospital Comparison feature."),
                    text("Select up to three hospitals to compare stats side by side.", class_name="pl-4 italic"),
                    class_name="flex-col"
                ),
                rx.flex(
                    text("State Rankings feature."),
                    text("Find the best hospitals in each state ranked by pay or overall experience.", class_name="pl-4 italic"),
                    class_name="flex-col"
                ),
                class_name="flex-col space-y-2 p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        rx.flex(
            rx.flex(
                class_name="h-8 md:h-16 w-[1px] bg-zinc-200 dark:bg-zinc-700"
            ),
            class_name="flex items-center justify-center w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("target", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Refine UI/UX", class_name="text-lg font-bold"),
                    text("August 2025 - November 2025", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle", class_name="stroke-zinc-200 dark:stroke-zinc-700"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                text("Refine user experience via user feedback after Major Feature Release #1."),
                text("Research user requested features to be added in Major Feature Release #3."),
                class_name="flex-col p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        rx.flex(
            rx.flex(
                class_name="h-8 md:h-16 w-[1px] bg-zinc-200 dark:bg-zinc-700"
            ),
            class_name="flex items-center justify-center w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("target", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Major Feature Release #2", class_name="text-lg font-bold"),
                    text("December 2025", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle", class_name="stroke-zinc-200 dark:stroke-zinc-700"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                text("Cost-of-living features."),
                text("Tie into API allowing adjusted cost-of-living comparisons. Pending funding/sponsorship requirements.", class_name="pl-4 italic"),
                class_name="flex-col p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        rx.flex(
            rx.flex(
                class_name="h-8 md:h-16 w-[1px] bg-zinc-200 dark:bg-zinc-700"
            ),
            class_name="flex items-center justify-center w-full"
        ),
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.icon("target", class_name="stroke-zinc-700 dark:stroke-zinc-500"),
                    class_name="flex items-center justify-center p-4"
                ),
                rx.flex(
                    text("Major Feature Release #3", class_name="text-lg font-bold"),
                    text("April 2026", class_name="text-sm uppercase"),
                    class_name="flex-col p-2 w-full"
                ),
                rx.flex(
                    rx.icon("circle", class_name="stroke-zinc-200 dark:stroke-zinc-700"),
                    class_name="flex items-center justify-center p-4"
                ),
                class_name="flex-row bg-zinc-50 dark:bg-zinc-800"
            ),
            rx.flex(
                text("Research Portal"),
                text("Enable nursing schools, professional nursing orgs, and research centers API access to anonymized reports for Quality Improvement research.", class_name="pl-4 italic"),
                class_name="flex-col p-2"
            ),
            class_name="flex-col divide-y dark:divide-zinc-700 border dark:border-zinc-700 rounded shadow-lg"
        ),
        class_name="flex-col w-full max-w-[700px]",
    )
