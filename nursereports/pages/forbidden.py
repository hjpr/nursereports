
from typing import Generator

import asyncio
import reflex as rx

async def redirect() -> Generator:
    asyncio.sleep(3)
    yield rx.redirect('/')

def forbidden() -> rx.Component:
    return rx.center(
        rx.heading(
            "403 - Page requires login"
        ),
        rx.text(
            "You will be redirected in a few seconds...."
        ),
    )