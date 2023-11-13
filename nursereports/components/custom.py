
from typing import Any, Dict, List, Literal

from reflex.components.component import Component
from reflex.vars import Var

import reflex as rx

class ChakraComponent(Component):
    """A component that wraps a Chakra component."""

    library = "@chakra-ui/react"


class ToastProvider(ChakraComponent):
    """A wrapped version of a a Chakra toast."""

    tag = "useToast"

    def _get_hooks(self) -> str | None:
        return "refs['__toast'] = useToast()"

    @staticmethod
    def show(
        title: str,
        description: str,
        duration: int,
        status: Literal["info", "warning", "success", "error", "loading"] = "info",
    ) -> rx.event.EventSpec:
        return rx.call_script(
            f"""
            refs['__toast']({{
            title: "{title}",
            description: "{description}",
            duration: {duration},
            status: "{status}",
            isClosable: true,
            }})
        """
        )


def spacer(**props) -> Component:
    """Provide spacer height as int or str. Will be processed as px. Default
    background is white.
    """

    return rx.Box(**props)