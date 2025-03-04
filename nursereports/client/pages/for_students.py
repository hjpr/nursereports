from ..components import navbar, footer, flex, text


import reflex as rx


@rx.page(route="/for-students", title="Nurse Reports")
def for_students_page() -> rx.Component:
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
        student_text(),
        class_name="flex-col items-center px-8 py-16 md:pt-24 md:pb-48 space-y-8 md:space-y-12 w-full max-w-screen-lg",
    )


def header() -> rx.Component:
    return rx.flex(
        text("For Nursing Students.", class_name="text-4xl font-bold"),
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


def student_text() -> rx.Component:
    return rx.flex(
        text(
            "Hospitals may make it seem like it's new graduates who should be thankful for the opportunity to work, but the reality is that new graduates are an incredible resource. Within a year of practicing, the hospital can develop a nurse to perform many of the same nursing tasks as nurses who have more experience and get paid at higher rates. Often new graduates are expected to fill shortages in less popular assignments, making them valuable for hospitals to cover areas with higher turnover and less interest.",
            class_name="leading-relaxed",
        ),
        text(
            "If you're a new graduate you have to realize that you are an asset to the hospital. As such you need to know the full situation of what you are walking into. Your first year is critical to establishing a connection to your job and the patients you serve. You shouldn't go to school for years just to come out and work at a hospital that destroys your hope for a fulfilling and balanced career.",
            class_name="leading-relaxed",
        ),
        text(
            "Although the hospital doesn't want to talk about it, pay is also extremely important to new graduates. You are coming out of school with student loans, car payments, and housing costs after not being able to work a full time job while in school. No one wants to look at their first paycheck - work a grueling few months - and question what they got themselves into. We'll provide a comprehensive list of pay data alongside information on culture and experience to help you find a first job that balances pay, culture, and workplace satisfaction. The only thing we ask is that once you get hired you take five minutes to submit a report. We'll do the rest.",
            class_name="leading-relaxed",
        ),
        text("- JM", class_name="pt-8"),
        class_name="flex-col space-y-6 text-zinc-700 w-full max-w-[700px]",
    )
