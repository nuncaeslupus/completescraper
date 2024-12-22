from typing import Any

from bs4 import BeautifulSoup
from pydantic import BaseModel


class HtmlContainer(BaseModel):
    name: str = ""
    children: dict[str, Any] = {}

    def __init__(
        self,
        html: str | BeautifulSoup = "",
        container_type: str = "",
        children_type: str = "",
        container_id: str = "",
        container_position: int = 0,
        container_id_attr: str = "",
        children_id_attr: str = "",
        children_value_attr: str | None = None,  # None for element text
        /,
        **kwargs,
    ) -> None:
        if html:
            kwargs = self.parse(
                html,
                container_type,
                children_type,
                container_id,
                container_position,
                container_id_attr,
                children_id_attr,
                children_value_attr,
            )
        super().__init__(**kwargs)

    def __bool__(self) -> bool:
        return bool(self.name) or bool(self.children)

    def parse(
        self,
        html: str | BeautifulSoup,
        container_type: str,
        children_type: str,
        container_id: str = "",
        container_position: int = 0,
        container_id_attr: str = "name",
        children_id_attr: str = "name",
        children_value_attr: str | None = None,
    ) -> dict[str, Any]:
        if html is None:
            return {"name": "", "children": {}}

        if isinstance(html, str):
            soup = BeautifulSoup(html, "html.parser")
        else:
            soup = html

        # First identify container by type and id
        if soup.name == container_type:  # E.g. "form", "select", "ul"...
            container = soup
        else:
            # Take all of them, no matter their id attribute
            if not container_id:
                if not (containers := soup.find_all(container_type)):
                    return {"name": "", "children": {}}
            elif not (
                containers := soup.find_all(
                    container_type, attrs={container_id_attr: container_id}
                )
            ):
                return {"name": "", "children": {}}

        container = containers[container_position]

        # Then find possible children
        children = {}
        for child in container.find_all(children_type):
            # Take text value instead of an attribute
            if not children_value_attr:
                if children_id_attr in child.attrs:
                    # Multiple class names if children_name_attr is "class", for example
                    if isinstance(child[children_id_attr], list):
                        children[" ".join(child[children_id_attr])] = " ".join(
                            text for text in child.stripped_strings
                        )
                    else:
                        children[child[children_id_attr]] = " ".join(
                            text for text in child.stripped_strings
                        )
            else:
                if children_id_attr in child.attrs:
                    # Multiple class names
                    if isinstance(child[children_id_attr], list):
                        children[" ".join(child[children_id_attr])] = child.get(
                            children_value_attr, ""
                        )
                    else:
                        children[child[children_id_attr]] = child.get(
                            children_value_attr, ""
                        )

        name = container.attrs[container_id_attr]
        return {
            "name": name or container_type,
            "children": children,
        }


class HtmlForm(HtmlContainer):
    def __init__(
        self,
        html: str | BeautifulSoup = "",
        form_id: str = "",
        form_position: int = 0,
        form_id_attr: str = "name",
        input_id_attr: str = "name",
        input_value_attr: str = "value",
        **kwargs,
    ) -> None:
        super().__init__(
            html,
            "form",
            "input",
            form_id,
            form_position,
            form_id_attr,
            input_id_attr,
            input_value_attr,
            **kwargs,
        )


class HtmlSelect(HtmlContainer):
    def __init__(
        self,
        html: str | BeautifulSoup = "",
        select_id: str = "",
        select_position: int = 0,
        select_id_attr: str = "name",
        option_id_attr: str = "name",
        option_value_attr: str | None = "value",
        **kwargs,
    ) -> None:
        super().__init__(
            html,
            "select",
            "option",
            select_id,
            select_position,
            select_id_attr,
            option_id_attr,
            option_value_attr,
            **kwargs,
        )


class HtmlUl(HtmlContainer):
    def __init__(
        self,
        html: str | BeautifulSoup = "",
        ul_id: str = "",
        ul_position: int = 0,
        ul_id_attr="name",
        li_id_attr: str = "name",
        li_value_attr: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            html,
            "ul",
            "li",
            ul_id,
            ul_position,
            ul_id_attr,
            li_id_attr,
            li_value_attr,
            **kwargs,
        )


class HtmlOl(HtmlContainer):
    def __init__(
        self,
        html: str | BeautifulSoup = "",
        ol_id: str = "",
        ol_position: int = 0,
        ol_id_attr="name",
        li_id_attr: str = "name",
        li_value_attr: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            html,
            "ol",
            "li",
            ol_id,
            ol_position,
            ol_id_attr,
            li_id_attr,
            li_value_attr,
            **kwargs,
        )
