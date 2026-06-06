"""Tests for the metrics module."""

from readability_auditor.metrics import calculate_metrics


def test_calculate_metrics_basic():
    """Test metrics calculation with sample text."""
    text = "The quick brown fox jumps over the lazy dog. " * 10
    metrics = calculate_metrics(text)

    assert metrics is not None
    assert metrics.word_count > 0
    assert metrics.token_count > 0
    assert metrics.flesch_reading_ease != 0
    assert metrics.lexical_density > 0
    assert metrics.token_to_word_ratio > 0


def test_calculate_metrics_empty_text():
    """Test that empty text returns None."""
    metrics = calculate_metrics("")
    assert metrics is None


def test_calculate_metrics_short_text():
    """Test that very short text returns None."""
    metrics = calculate_metrics("Hello world")
    assert metrics is None
