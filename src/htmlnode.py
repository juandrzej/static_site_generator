from __future__ import annotations


class HTMLNode:
    """Base class for representing HTML elements or text as nodes in a parse tree."""

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Return the properties as an HTML attribute string."""
        if self.props is None:
            return ""
        inner_strings = [f'{key}="{value}"' for key, value in self.props.items()]
        return " " + " ".join(inner_strings)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """
    Represents a leaf node containing only text, or text with a single tag (like <b> or <code>).
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        if value is None:
            raise ValueError("LeafNode.__init__() missing required argument: 'value'")
        super().__init__(value=value, tag=tag, children=None, props=props)

    def to_html(self) -> str:
        """Convert this leaf node to its HTML string representation."""
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    Represents a node containing other HTMLNode objects as children (like <div> or <ul>).
    """

    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        if tag is None:
            raise ValueError("ParentNode.__init__() missing required argument: 'tag'")
        if children is None:
            raise ValueError(
                "ParentNode.__init__() missing required argument: 'children'"
            )
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        """Convert this node and its children to an HTML string representation."""
        assert self.children is not None
        inner_string = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{inner_string}</{self.tag}>"
