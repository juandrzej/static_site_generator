class HTMLNode:
    def __init__(
        self,
        value: str | None = None,
        tag: str | None = None,
        props: dict[str, str] | None = None,
        children: list[object] | None = None,
    ) -> None:
        self.value = value
        self.tag = tag
        self.props = props
        self.children = children

    def to_html(self) -> str | None:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        inner_strings = [f'{key}="{value}"' for key, value in self.props.items()]
        return " " + " ".join(inner_strings)

    def __repr__(self) -> str:
        return f"HTMLNode({self.value}, {self.tag}, {self.props}, {self.children})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(value=value, tag=tag, props=props, children=None)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
