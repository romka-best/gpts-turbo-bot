import re
from typing import List, Tuple


def close_tags(
    html: str,
    open_tags: List[str] = None
) -> Tuple[str, List[str]]:
    tag_pattern = re.compile(r'<(/?)(\w+)([^>]*)>')
    open_stack = []
    close_queue = []
    close_open_tags = []

    for tag in tag_pattern.finditer(html):
        is_closing_tag = tag.group(1) == '/'
        tag_name = tag.group(2)
        tag_atr = tag.group(3)

        if not is_closing_tag:
            open_stack.insert(0, tag_name)
            close_open_tags.append(f"<{tag_name}{tag_atr}>")
        elif open_stack and open_stack[0] == tag_name:
            open_stack.pop(0)
        else:
            close_queue.append(tag_name)

    for tag_name in open_stack:
        html += '</' + tag_name + '>'

    if open_tags:
        html = "".join(open_tags) + html
    else:
        for tag_name in close_queue:
            html = '<' + tag_name + '>' + html

    return html, close_open_tags[-len(open_stack):]


def split_message(text: str, chunk_size=4096):
    parts = []

    while text:
        if len(text) <= chunk_size:
            parts.append(text)
            break

        part = text[:chunk_size]
        first_ln = part.rfind('\n')

        if first_ln != -1:
            new_part = part[:first_ln]
            parts.append(new_part)

            text = text[first_ln + 1:]
            continue

        first_space = part.rfind(' ')

        if first_space != -1:
            new_part = part[:first_space]
            parts.append(new_part)

            text = text[first_space + 1:]
            continue

        parts.append(part)
        text = text[chunk_size:]

    result_parts = []
    open_tags = None
    for part in parts:
        text, open_tags = close_tags(part, open_tags)
        result_parts.append(text)

    return result_parts
