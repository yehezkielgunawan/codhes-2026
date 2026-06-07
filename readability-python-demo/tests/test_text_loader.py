"""Tests for text loader module."""

import pytest
from pathlib import Path
from readability_auditor.text_loader import (
    load_raw_texts,
    get_domain_from_url,
    find_text_pairs,
)


class TestGetDomainFromUrl:
    """Tests for URL to domain conversion."""

    def test_simple_url(self):
        """Simple URL should extract domain."""
        assert get_domain_from_url("https://react.dev") == "react.dev"

    def test_url_with_path(self):
        """URL with path should extract just the domain."""
        assert get_domain_from_url("https://docs.github.com/en") == "docs.github.com"

    def test_url_with_trailing_slash(self):
        """URL with trailing slash should work."""
        assert get_domain_from_url("https://react.dev/") == "react.dev"

    def test_url_with_subdomain(self):
        """URL with subdomain should preserve it."""
        assert get_domain_from_url("https://developers.cloudflare.com") == "developers.cloudflare.com"


class TestFindTextPairs:
    """Tests for finding text pairs in raw_texts directory."""

    def test_find_pairs_with_both_files(self, tmp_path):
        """Should find pairs where both human and machine files exist."""
        # Create test files
        (tmp_path / "react.dev_human.md").write_text("Human text")
        (tmp_path / "react.dev_machine.txt").write_text("Machine text")
        (tmp_path / "github.com_human.md").write_text("Human text 2")
        (tmp_path / "github.com_machine.txt").write_text("Machine text 2")

        pairs = find_text_pairs(tmp_path)

        assert len(pairs) == 2
        assert "react.dev" in pairs
        assert "github.com" in pairs

    def test_find_pairs_with_only_machine(self, tmp_path):
        """Should include pairs with only machine text."""
        (tmp_path / "cursor.com_machine.txt").write_text("Machine only")

        pairs = find_text_pairs(tmp_path)

        assert len(pairs) == 1
        assert "cursor.com" in pairs
        assert pairs["cursor.com"]["machine"] is not None
        assert pairs["cursor.com"]["human"] is None

    def test_find_pairs_empty_directory(self, tmp_path):
        """Should return empty dict for empty directory."""
        pairs = find_text_pairs(tmp_path)

        assert len(pairs) == 0


class TestLoadRawTexts:
    """Tests for loading raw text files."""

    def test_load_human_text(self, tmp_path):
        """Should load human text from .md file."""
        (tmp_path / "react.dev_human.md").write_text("# React Documentation\n\nThis is human text.")
        (tmp_path / "react.dev_machine.txt").write_text("Machine text")

        pairs = find_text_pairs(tmp_path)
        human_text = load_raw_texts(pairs["react.dev"]["human"])

        assert "React Documentation" in human_text
        assert "human text" in human_text

    def test_load_machine_text(self, tmp_path):
        """Should load machine text from .txt file."""
        (tmp_path / "react.dev_machine.txt").write_text("# React\n\nThis is machine text.")

        pairs = find_text_pairs(tmp_path)
        machine_text = load_raw_texts(pairs["react.dev"]["machine"])

        assert "React" in machine_text
        assert "machine text" in machine_text

    def test_load_none_path(self):
        """Should return None for None path."""
        result = load_raw_texts(None)

        assert result is None
