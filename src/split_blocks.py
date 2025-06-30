def markdown_to_blocks(markdown: str) -> list[str]:
    # targets specifically trailing whitespaces on few line paragraphs
    markdown = "\n".join(map(str.strip, markdown.split("\n")))
    # splits paragraphs after removing whole stings traling whitespaces
    blocks = markdown.strip().split("\n\n")
    # removes trailing whitespaces if there were more than 2 empty lines in between
    blocks = map(str.strip, blocks)
    # filter blanks
    return list(filter(None, blocks))
