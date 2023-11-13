
from typing import List, Literal

from reflex.components import Box
from reflex.components.component import Base, Component

class Page(Base):
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
    layout: Component

    @classmethod
    def get_route(cls) -> str:
        """Returns route of page based on file structure and class name.
        For ex. myblogpage -> '/myblogpage' or in subfolder blogs ->
        '/blogs/myblogpage'
        """

        module_path = cls.__module__
        path_parts = module_path.split('.')[1:] # [1:] excludes base folder
        return '/' + '/'.join(path_parts).lower()


    def render(self) -> Component:
        """Returns Box component with nested Components to render from layout attribute."""

        return Box(
            self.layout,
        )