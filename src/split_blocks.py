import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits a markdown string into a list of blocks by blank lines.
    Strips trailing and leading whitespace from each line and removes empty blocks.
    """
    lines = [line.strip() for line in markdown.splitlines()]
    cleaned_markdown = "\n".join(lines).strip()
    blocks = [
        block.strip() for block in cleaned_markdown.split("\n\n") if block.strip()
    ]
    return blocks


def _is_heading(block: str) -> bool:
    return bool(re.match(r"^#{1,6} .+", block))


def _is_code_block(block: str) -> bool:
    return len(block) >= 6 and block.startswith("```") and block.endswith("```")


def _is_quote(block: str) -> bool:
    return all(line.startswith(">") for line in block.splitlines())


def _is_ulist(block: str) -> bool:
    return all(line.startswith("- ") for line in block.splitlines())


def _is_olist(block: str) -> bool:
    lines = block.splitlines()
    return all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines))


def block_to_block_type(block: str) -> BlockType:
    """
    Determines the markdown block type of a block and returns the corresponding BlockType.
    """
    if _is_heading(block):
        return BlockType.HEADING
    if _is_code_block(block):
        return BlockType.CODE
    if _is_quote(block):
        return BlockType.QUOTE
    if _is_ulist(block):
        return BlockType.ULIST
    if _is_olist(block):
        return BlockType.OLIST
    return BlockType.PARAGRAPH
