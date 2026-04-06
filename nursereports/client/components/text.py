import reflex as rx

_TEXT = "text-neutral-700 dark:text-neutral-300"

_HEADING = (
    "font-semibold tracking-tight "
    "text-neutral-950 dark:text-neutral-50"
)

# Maps semantic size names to responsive Tailwind classes.
_HEADING_SIZES: dict[str, str] = {
    "sm":  "text-lg",
    "md":  "text-xl",
    "lg":  "text-2xl",
    "xl":  "text-3xl",
    "2xl": "text-4xl md:text-5xl",
    "3xl": "text-5xl md:text-6xl",
}


def text(*children, **props) -> rx.Component:
    """Body text with default neutral color."""
    user_classes = props.pop("class_name", "")
    return rx.text(
        *children,
        class_name=f"{_TEXT} {user_classes}".strip(),
        **props,
    )


def heading(*children, level: str = "lg", **props) -> rx.Component:
    """
    Heading text — font-semibold, tracking-tight, primary color.

    level: "sm" | "md" | "lg" | "xl" | "2xl" | "3xl"
           Defaults to "lg" (text-2xl). Override further with class_name.
    """
    size_class = _HEADING_SIZES.get(level, _HEADING_SIZES["lg"])
    user_classes = props.pop("class_name", "")
    return rx.text(
        *children,
        class_name=f"{_HEADING} {size_class} {user_classes}".strip(),
        **props,
    )
