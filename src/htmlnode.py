class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[object] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str | None:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        inner_strings = [f'{key}="{value}"' for key, value in self.props.items()]
        return " " + " ".join(inner_strings)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        if value is None:
            raise ValueError("Child.__init__() missing required argument: 'value'")
        super().__init__(value=value, tag=tag, children=None, props=props)

    def to_html(self) -> str | None:
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        children: list[object] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        if tag is None:
            raise ValueError("Child.__init__() missing required argument: 'tag'")
        if children is None:
            raise ValueError("Child.__init__() missing required argument: 'children'")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str | None:
        inner_string = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{inner_string}</{self.tag}>"
