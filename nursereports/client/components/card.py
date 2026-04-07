import reflex as rx

_CARD = (
    "bg-white dark:bg-[#1a1a1a] "
    "border border-neutral-200 dark:border-neutral-800 "
    "rounded-2xl"
)

_CARD_HEADER = (
    "flex items-center "
    "px-5 py-4 "
    "border-b border-neutral-300 dark:border-neutral-800 "
    "w-full"
)

_CARD_SECTION = (
    "flex "
    "px-5 py-4 "
    "border-b border-neutral-200 dark:border-neutral-800 "
    "w-full"
)


def card(*children, **props) -> rx.Component:
    """
    Standard card container.
    White/dark-[#1a1a1a] background, subtle border, rounded-2xl.
    No shadow — depth comes from background contrast.
    """
    user_classes = props.pop("class_name", "")
    return rx.flex(
        *children,
        class_name=f"{_CARD} {user_classes}".strip(),
        **props,
    )


def card_header(*children, **props) -> rx.Component:
    """
    Card header row — sits at the top of a card, separated by a bottom border.
    No background fill. Pass icon + heading as children.
    """
    user_classes = props.pop("class_name", "")
    return rx.flex(
        *children,
        class_name=f"{_CARD_HEADER} {user_classes}".strip(),
        **props,
    )


def card_section(*children, **props) -> rx.Component:
    """
    Internal card section with a bottom border divider.
    Use to stack multiple content blocks inside a card.
    """
    user_classes = props.pop("class_name", "")
    return rx.flex(
        *children,
        class_name=f"{_CARD_SECTION} {user_classes}".strip(),
        **props,
    )
