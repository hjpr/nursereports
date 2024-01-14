
from typing import List, Literal
from ..components import navbar, footer
from ..components.navbar import c2a_spacer

import reflex as rx

class Page(rx.Base):
    """The base page class to contain metadata, layout, and functions to
    render a single page. When creating a page, the class name is the page
    route, unless it is 'index' in which case it will have route '/'. Ensure
    that if the file structure includes subfolders, that each subfolder contains
    an __init__.py.

    title - 
    description - 
    keywords - 
    robots - 
    route -
    """

    # Title of the page
    title: str

    # Description of the page
    description: str

    # Keywords for the page
    keywords: List[str]

    # Tag for crawlers
    robots: Literal["index", "noindex", "follow", "nofollow"]

    # Nested component layout to return to render page.
    layout: rx.Component

    @classmethod
    def get_route(cls) -> str:
        """Returns route of page based on file structure and class name.
        For ex. myblogpage -> '/myblogpage' or in subfolder blogs ->
        '/blogs/myblogpage'
        """

        module_path = cls.__module__
        path_parts = module_path.split('.')[1:] # [1:] excludes base folder
        return '/' + '/'.join(path_parts).lower()


    def render() -> rx.Component:
        return rx.flex(

            navbar(),

            c2a_spacer(),
            
            # CONTENT CONTAINER
            rx.flex(

                # STYLING FOR CONTENT CONTAINER
                flex_direction='column',
                flex_basis='auto',
                flex_grow='1',
                flex_shrink='0',
            ),

            footer(),

            # STYLING FOR BODY CONTAINER
            flex_direction='column',
            min_height='100vh',

        )