from ..components import navbar, footer, flex, text

import reflex as rx


@rx.page(route="/about-us", title="Nurse Reports")
def about_us_page() -> rx.Component:
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
        about_text(),
        class_name="flex-col items-center px-8 py-16 md:pt-24 md:pb-48 space-y-8 md:space-y-12 w-full max-w-screen-lg",
    )


def header() -> rx.Component:
    return rx.flex(
        text("A Little About Us.", class_name="text-4xl font-bold"),
        text(
            "A quick introduction into our founding principles, and who we are.",
            class_name="text-start md:text-center",
        ),
        class_name="flex-col items-start md:items-center text-lg space-y-6 w-full",
    )


def image() -> rx.Component:
    return rx.flex(
        flex(
            text("PLACEHOLDER", class_name="text-xs"),
            class_name="flex-col items-center justify-center rounded-lg border bg-white aspect-video w-full max-w-[700px]",
        ),
        class_name="flex-col items-center w-full",
    )


def about_text() -> rx.Component:
    return rx.flex(
        text(
            "I'm J, an ICU nurse. I've worked bedside for the past 5 years through quite a transformational period in the nursing profession. I cut my teeth in the COVID ICU for a couple years, traveled, then pivoted to an ICU float position to try to round out my knowledge-base.",
            class_name="leading-relaxed",
        ),
        text(
            "I started this project in 2021 convinced that by creating open and freely accessible lines of communication we could create a powerful career tool for the benefit of millions of nurses nationwide. I'm still here in 2025 after a long development road, to release this tool and continue working towards shifting the power dynamic back to the people who form the foundations of our entire national healthcare apparatus.",
            class_name="leading-relaxed",
        ),
        text(
            "I've worked on this project solo for almost 4 years, but I use 'us' to describe just how many people have shaped and contributed to this project. I'll also rely on you - the bedside nurse - to help me build an ecosystem through data, where you and your colleagues can get real-time info on pay, unit culture, staffing, and much more.",
            class_name="leading-relaxed",
        ),
        class_name="flex-col space-y-6 text-zinc-700 w-full max-w-[700px]",
    )
