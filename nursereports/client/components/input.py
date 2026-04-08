import reflex as rx

_BASE = (
    "bg-neutral-50 dark:bg-neutral-900 "
    "border border-neutral-300 dark:border-neutral-800 "
    "text-neutral-900 dark:text-neutral-100 "
    "placeholder:text-neutral-400 dark:placeholder:text-neutral-600 "
    "rounded-full "
    "focus:outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500 "
    "transition-colors duration-150"
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


def input(
    *children,
    size: str = "md",
    width: str = "full",
    **props,
) -> rx.Component:
    """
    Text input.
      size:  sm | md | lg | xl           (default: md)
      width: auto | full | 3/4 | 2/3 | 1/2 | 1/3  (default: auto)
    Heights match button sizes: sm=h-8, md=h-10, lg=h-12, xl=h-14.
    User-provided class_name is ignored.
    """
    props.pop("class_name", None)

    size_cls = _SIZES.get(size, _SIZES["md"])
    width_cls = _WIDTHS.get(width, "")

    class_name = " ".join(filter(None, [_BASE, size_cls, width_cls]))
    return rx.el.input(*children, class_name=class_name, **props)
