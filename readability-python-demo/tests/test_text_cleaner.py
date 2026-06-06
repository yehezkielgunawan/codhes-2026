"""Tests for the text cleaner module."""

from readability_auditor.text_cleaner import clean_human_documentation


def test_clean_removes_code_blocks():
    """Test that code blocks are removed."""
    text = """
# Title

Some prose text here.

```python
def hello():
    print("world")
```

More prose text here.
"""
    cleaned = clean_human_documentation(text)
    assert "def hello()" not in cleaned
    assert "Some prose text here" in cleaned
    assert "More prose text here" in cleaned


def test_clean_removes_navigation_links():
    """Test that navigation-only lines are removed."""
    text = """
[Quick Start](https://example.com/learn)
[Tutorial](https://example.com/tutorial)
[Reference](https://example.com/reference)

This is actual documentation prose that should be kept.
"""
    cleaned = clean_human_documentation(text)
    assert "Quick Start" not in cleaned or "actual documentation prose" in cleaned
    assert "actual documentation prose" in cleaned


def test_clean_removes_inline_code():
    """Test that inline code is removed but text is kept."""
    text = "Use the `useState` hook to manage state in your component."
    cleaned = clean_human_documentation(text)
    assert "`useState`" not in cleaned
    assert "hook to manage state" in cleaned


def test_clean_removes_images():
    """Test that image references are removed."""
    text = """
![Logo](https://example.com/logo.png)

This is documentation text.
"""
    cleaned = clean_human_documentation(text)
    assert "![Logo]" not in cleaned
    assert "documentation text" in cleaned


def test_clean_keeps_paragraphs():
    """Test that prose paragraphs are kept."""
    text = """
React is a JavaScript library for building user interfaces.

Components let you split the UI into independent, reusable pieces.

State allows a component to remember information between renders.
"""
    cleaned = clean_human_documentation(text)
    assert "React is a JavaScript library" in cleaned
    assert "Components let you split" in cleaned
    assert "State allows a component" in cleaned


def test_clean_empty_input():
    """Test that empty input returns empty string."""
    assert clean_human_documentation("") == ""
    assert clean_human_documentation(None) == ""


def test_clean_preserves_link_text():
    """Test that link text is preserved while URLs are removed."""
    text = "Learn more about [React Hooks](https://react.dev/hooks) in the docs."
    cleaned = clean_human_documentation(text)
    assert "React Hooks" in cleaned
    assert "https://react.dev/hooks" not in cleaned
