import reflex as rx

_BASE = (
    "inline-flex items-center justify-center gap-2 "
    "rounded-full "
    "font-medium "
    "transition-colors duration-150 "
    "cursor-pointer "
    "whitespace-nowrap"
)

_SIZES: dict[str, str] = {
    "sm": "h-8  px-3 text-xs",
    "md": "h-10 px-4 text-sm",
    "lg": "h-12 px-5 text-base",
    "xl": "h-14 px-6 text-lg",
}

_WIDTHS: dict[str, str] = {
    "auto": "",
    "full": "w-full",
    "3/4":  "w-3/4",
    "2/3":  "w-2/3",
    "1/2":  "w-1/2",
    "1/3":  "w-1/3",
}

_OUTLINE = (
    "bg-white dark:bg-[#1a1a1a] "
    "ring-[1.5px] ring-neutral-300 dark:ring-neutral-700 "
    "text-neutral-600 dark:text-neutral-100 "
    "hover:bg-neutral-50 dark:hover:bg-neutral-800"
)

_GHOST = (
    "bg-transparent "
    "text-neutral-600 dark:text-neutral-400 "
    "hover:bg-neutral-100 dark:hover:bg-neutral-900 "
    "hover:text-neutral-900 dark:hover:text-neutral-100"
)


def _solid_classes(color: str) -> str:
    return (
        f"bg-{color}-600 dark:bg-{color}-500 "
        f"text-white "
        f"hover:bg-{color}-700 dark:hover:bg-{color}-400"
    )


def button(
    *children,
    variant: str = "solid",
    size: str = "md",
    color: str = "emerald",
    width: str = "auto",
    **props,
) -> rx.Component:
    """
    Button component.
      variant: solid | outline | ghost     (default: solid)
      size:    sm | md | lg | xl           (default: md)
      color:   Tailwind color base, e.g. 'teal' | 'blue' | 'red'  (default: teal, solid only)
      width:   auto | full | 3/4 | 2/3 | 1/2 | 1/3  (default: auto)
    """
    props.pop("class_name", None)

    size_cls = _SIZES.get(size, _SIZES["md"])
    width_cls = _WIDTHS.get(width, "")

    if variant == "outline":
        variant_cls = _OUTLINE
    elif variant == "ghost":
        variant_cls = _GHOST
    else:
        variant_cls = _solid_classes(color)

    class_name = " ".join(filter(None, [_BASE, size_cls, variant_cls, width_cls]))
    return rx.button(*children, class_name=class_name, **props)


# ---------------------------------------------------------------------------
# Backwards-compatible aliases — delegate to button() with the right variant.
# Existing call sites continue to work; migrate them to button() over time.
# Note: class_name is intentionally dropped (no user classes accepted).
# ---------------------------------------------------------------------------

def solid_button(*children, **props) -> rx.Component:
    return button(*children, variant="solid", **props)


def outline_button(*children, **props) -> rx.Component:
    return button(*children, variant="outline", **props)


def ghost_button(*children, **props) -> rx.Component:
    return button(*children, variant="ghost", **props)
