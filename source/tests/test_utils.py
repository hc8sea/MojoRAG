import pytest
import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..utils import word_wrap, process_title

logging.basicConfig(level=logging.WARNING)

@pytest.mark.parametrize(
    "input_str, width, expected",
    [
        ("This is a simple string.", 72, "This is a simple string."),
        ("The quick brown fox jumps over the lazy dog.", 20, "The quick brown fox\njumps over the lazy\ndog."),
        ("Data science is amazing ", 25, "Data science is amazing "),  # Exact Width at Space
        ("Short", 10, "Short"),
    ]
)

def test_word_wrap(input_str, width, expected):
    """Tests for the word_wrap function."""
    assert word_wrap(input_str, width) == expected


@pytest.mark.parametrize(
    "input_title, expected",
    [
        ("# This is a valid title", "This is a valid title"),
        ("# Another Title <a href='link'>", "Another Title"),
        ("This is not a title", None),
        ("# Title without tags", "Title without tags"),
    ]
)
def test_process_title(input_title, expected):
    """Tests for the process_title function."""
    assert process_title(input_title) == expected
