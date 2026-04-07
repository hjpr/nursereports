import reflex as rx

_INPUT = (
    "bg-neutral-50 dark:bg-neutral-900 "
    "border border-neutral-300 dark:border-neutral-800 "
    "text-neutral-900 dark:text-neutral-100 text-base "
    "placeholder:text-neutral-400 dark:placeholder:text-neutral-600 "
    "rounded-2xl "
    "px-4 py-3 min-h-[48px] "
    "focus:outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500 "
    "transition-colors duration-150"
)


def input(*children, **props) -> rx.Component:
    """Styled text input."""
    user_classes = props.pop("class_name", "")
    return rx.input(
        *children,
        class_name=f"{_INPUT} {user_classes}".strip(),
        **props,
    )
