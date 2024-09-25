import re


def get_open_markdown(text_part):
    open_formatting = {
        '**': 0,
        '*': 0,
        '__': 0,
        '_': 0,
        '`': 0,
        '```': 0,
    }

    open_code_block = None

    matches = re.findall(r"(```[\w]*)|(\*\*|\*|__|_|```|`)", text_part)

    for match in matches:
        symbol = match[0] or match[1]

        if symbol.startswith('```') and len(symbol) > 3:
            if open_formatting['```'] % 2 == 0:
                open_code_block = symbol
            open_formatting['```'] += 1
        elif symbol == '```':
            open_formatting['```'] += 1
        elif symbol in open_formatting:
            open_formatting[symbol] += 1

    open_tags = []
    for symbol, count in open_formatting.items():
        if count % 2 != 0:
            if symbol == '```' and open_code_block:
                open_tags.append(open_code_block + '\n')
            elif symbol != '_':
                open_tags.append(symbol)

    return open_tags


def close_open_markdown(tags):
    return ''.join([tag if not tag.startswith('```') else '```' for tag in tags])


def reopen_markdown(tags):
    return ''.join([tag for tag in tags])


def split_message(text: str, chunk_size=4096):
    parts = []
    current_part = ""

    for i, char in enumerate(text):
        current_part += char
        if len(current_part) >= chunk_size or i == len(text) - 1:
            open_tags = get_open_markdown(current_part)
            current_part += close_open_markdown(open_tags)
            parts.append(current_part)
            current_part = reopen_markdown(open_tags)

    return parts
