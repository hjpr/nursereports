from ..components import navbar, footer, flex, text
import reflex as rx


@rx.page(route="/for-staff", title="Nurse Reports")
def for_staff_page() -> rx.Component:
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
        staff_text(),
        class_name="flex-col items-center px-8 py-16 md:pt-24 md:pb-48 space-y-8 md:space-y-12 w-full max-w-screen-lg",
    )


def header() -> rx.Component:
    return rx.flex(
        text("For Staff Nurses.", class_name="text-4xl font-bold"),
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


def staff_text() -> rx.Component:
    return rx.flex(
        text(
            "Staff nurses are the core component of any hospital institution. Our roles spread across so many different areas that it's harder to think about what nurses aren't involved in than what we are. Nurses are essential to both in-hospital care, and continuing care after discharge. We provide direct patient-facing care, but also we're in the background ensuring that all the pieces of this complicated system are organized.",
            class_name="leading-relaxed",
        ),
        text(
            "The way that nurses get paid is similarly diverse. Nurses get paid in the form of full-time, part-time, hourly, weekly, bi-weekly, and yearly wages. That diversity of pay along with the varying cost of living can make it extremely difficult to decipher not only the environment of nursing pay, but also the fair market value of our labor.",
            class_name="leading-relaxed",
        ),
        text(
            "A major focus of NurseReports.org is not just as a simple repository of pay information. NurseReports.org condenses, compares, and organizes pay data provided by nurses from across the US to help you understand what's fair regardless of where you are practicing.",
            class_name="leading-relaxed",
        ),
        text(
            "Pay transparency doesn't go far enough in my opinion. We are building a powerful platform using your data and our tools so that in one or two clicks you can make impactful decisions that lead to competitive wages, solid benefits, and bring actual accountability to hospital systems nationwide. All of this starts with you taking five minutes to submit a simple report. We'll do the rest.",
            class_name="leading-relaxed",
        ),
        text("- JM", class_name="pt-8"),
        class_name="flex-col space-y-6 text-zinc-700 w-full max-w-[700px]",
    )
