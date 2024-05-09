import logging

def word_wrap(string: str, n_chars: int = 72) -> str:
    """
    Wrap a string at the nearest space after a specified number of characters.

    Parameters:
        string (str): The input string to wrap.
        n_chars (int): The maximum number of characters per line. Default is 72.

    Returns:
        str: The wrapped string, with newline characters added.
    """
    if len(string) <= n_chars:
        return string

    return string[:n_chars].rsplit(' ', 1)[0] + '\n' + word_wrap(string[len(string[:n_chars].rsplit(' ', 1)[0])+1:], n_chars)


def process_title(title: str) -> str | None:
    """
    Process a Markdown title by removing the leading header marker and any trailing HTML tags.

    Parameters:
        title (str): The input title string starting with '# '.

    Returns:
        str | None: The cleaned title if the input starts with '# ', otherwise None.
    """
    if title.startswith('# '):
        title = title.split('# ')[1]
        title = title.split('<a')[0]
        return title.strip()

    logging.warning(f"Title does not start with '# ': {title}")
    return None