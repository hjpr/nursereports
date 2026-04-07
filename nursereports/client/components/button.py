import reflex as rx

_SOLID = (
    "bg-teal-600 dark:bg-teal-500 "
    "text-white "
    "rounded-full "
    "px-6 py-2.5 "
    "font-medium text-sm "
    "hover:bg-teal-700 dark:hover:bg-teal-400 "
    "transition-colors duration-150 "
    "cursor-pointer"
)

_OUTLINE = (
    "bg-white dark:bg-[#1a1a1a] "
    "border border-neutral-300 dark:border-neutral-800 "
    "text-neutral-600 dark:text-neutral-100 "
    "rounded-full "
    "font-medium text-sm "
    "hover:bg-neutral-50 dark:hover:bg-neutral-800 "
    "transition-colors duration-150 "
    "cursor-pointer"
)

_GHOST = (
    "bg-transparent "
    "text-neutral-600 dark:text-neutral-400 "
    "rounded-full "
    "px-4 py-2 "
    "font-medium text-sm "
    "hover:bg-neutral-100 dark:hover:bg-neutral-900 "
    "hover:text-neutral-900 dark:hover:text-neutral-100 "
    "transition-colors duration-150 "
    "cursor-pointer"
)


def solid_button(*children, **props) -> rx.Component:
    """Primary teal pill button."""
    user_classes = props.pop("class_name", "")
    return rx.button(
        *children,
        class_name=f"{_SOLID} {user_classes}".strip(),
        **props,
    )


def outline_button(*children, **props) -> rx.Component:
    """Secondary pill button with border."""
    user_classes = props.pop("class_name", "")
    return rx.button(
        *children,
        class_name=f"{_OUTLINE} {user_classes}".strip(),
        **props,
    )


def ghost_button(*children, **props) -> rx.Component:
    """Transparent pill button for low-emphasis actions."""
    user_classes = props.pop("class_name", "")
    return rx.button(
        *children,
        class_name=f"{_GHOST} {user_classes}".strip(),
        **props,
    )
