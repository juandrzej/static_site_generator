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
    # targets specifically trailing whitespaces on few line paragraphs
    markdown = "\n".join(map(str.strip, markdown.split("\n")))
    # splits paragraphs after removing whole stings traling whitespaces
    blocks = markdown.strip().split("\n\n")
    # removes trailing whitespaces if there were more than 2 empty lines in between
    blocks = map(str.strip, blocks)
    # filter blanks
    return list(filter(None, blocks))


def _is_heading(block: str) -> bool:
    return bool(re.match(r"^#{1,6} .+", block))


def _is_code_block(block: str) -> bool:
    return len(block) >= 6 and block.startswith("```") and block.endswith("```")


def _is_quote(block: str) -> bool:
    return all([blk.startswith(">") for blk in block.split("\n")])


def _is_ulist(block: str) -> bool:
    return all([blk.startswith("- ") for blk in block.split("\n")])


def _is_olist(block: str) -> bool:
    blocks = block.split("\n")
    return all([blk.startswith(f"{blocks.index(blk) + 1}. ") for blk in blocks])


def block_to_block_type(block: str) -> BlockType:
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
