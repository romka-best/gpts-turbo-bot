from bs4 import BeautifulSoup


def split_message(html_text: str, limit=3968):
    soup = BeautifulSoup(html_text, 'html.parser')
    parts = []
    current_part = ''

    for element in soup.children:
        element_str = str(element)
        if len(current_part) + len(element_str) <= limit:
            current_part += element_str
        else:
            parts.append(current_part)
            current_part = element_str

    if current_part:
        parts.append(current_part)

    return parts
