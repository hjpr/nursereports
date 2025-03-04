from ..components import navbar, footer, flex, text

import reflex as rx


@rx.page(
    route="/for-travelers",
    title="Nurse Reports",
)
def for_travelers_page() -> rx.Component:
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
        traveler_text(),
        class_name="flex-col items-center px-8 py-16 md:pt-24 md:pb-48 space-y-8 md:space-y-12 w-full max-w-screen-lg",
    )


def header() -> rx.Component:
    return rx.flex(
        text("For Travel Nurses.", class_name="text-4xl font-bold"),
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


def traveler_text() -> rx.Component:
    return rx.flex(
        text(
            "In the current and future nursing shortage, travelers are a key component of the overall healthcare staffing strategy. When hospitals were overrun during the COVID pandemic, using temporary staff was the only way to maintain operational staffing levels. For many hospitals now, travelers maintain ratios and make up for call-outs and vacancies that hospitals can't fill. Many travelers use traveling as a way to visit new cities and explore areas they wouldn't otherwise have the ability to move to if they took a full-time position. Other travelers appreciate the bump in wages for the inconvenience of working a schedule that the hospital decides.",
            class_name="leading-relaxed",
        ),
        text(
            "Whatever the reason, travelers have different criteria for taking jobs than staff nurses. NurseReports.org centralizes a large repository of pay information that helps you determine not only what you get paid, but the pay context. That is to say, how do rates look like they are trending? As data is aggregated, we'll forecast the way that rates seem to be moving. We'll also offer in the future, cost-of-living adjusted rates so you can compare those rates fairly across locations.",
            class_name="leading-relaxed",
        ),
        text(
            "Travelers offer a straightforward and unique perspective into the positions they work. We want to offer you a unique set of tools to help you make the best decision for your next assignment. Details that allow you to maximize your pay, and give you details down to the unit-level to ensure you know what you are walking into. All of this starts with you taking five minutes to submit a simple report. We'll do the rest.",
            class_name="leading-relaxed",
        ),
        text("- JM", class_name="pt-8"),
        class_name="flex-col space-y-6 text-zinc-700 w-full max-w-[700px]",
    )
