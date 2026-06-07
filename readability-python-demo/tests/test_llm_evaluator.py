"""Tests for LLM evaluator module."""

import pytest
from readability_auditor.llm_evaluator import (
    chunk_text,
    calculate_lri,
    LLMEvaluator,
)


class TestChunkText:
    """Tests for text chunking functionality."""

    def test_chunk_short_text_returns_single_chunk(self):
        """Text shorter than max_tokens should return as single chunk."""
        text = "This is a short text."
        chunks = chunk_text(text, max_tokens=100)

        assert len(chunks) == 1
        assert chunks[0] == text

    def test_chunk_long_text_returns_multiple_chunks(self):
        """Text longer than max_tokens should be split into multiple chunks."""
        # Create text that's definitely longer than 20 tokens
        text = "This is a test. " * 10  # ~50 tokens
        chunks = chunk_text(text, max_tokens=20)

        assert len(chunks) > 1

    def test_chunk_respects_overlap(self):
        """Chunks should overlap by specified number of tokens."""
        text = "This is a test for overlap. " * 10  # ~60 tokens
        chunks = chunk_text(text, max_tokens=30, overlap=5)

        # Should create at least 2 chunks with overlap
        assert len(chunks) >= 2

    def test_chunk_handles_empty_text(self):
        """Empty text should return empty list."""
        chunks = chunk_text("", max_tokens=100)

        assert chunks == []

    def test_chunk_handles_very_short_text(self):
        """Very short text (less than 50 chars) should return as single chunk."""
        text = "Short"
        chunks = chunk_text(text, max_tokens=100)

        assert len(chunks) == 1


class TestCalculateLRI:
    """Tests for LLM Readability Index calculation."""

    def test_lri_minimum_score(self):
        """All 1s should give LRI of 0."""
        scores = {
            "clarity": 1,
            "completeness": 1,
            "conciseness": 1,
            "technical_accuracy": 1,
            "llm_friendliness": 1,
        }
        lri = calculate_lri(scores)

        assert lri == 0.0

    def test_lri_maximum_score(self):
        """All 5s should give LRI of 100."""
        scores = {
            "clarity": 5,
            "completeness": 5,
            "conciseness": 5,
            "technical_accuracy": 5,
            "llm_friendliness": 5,
        }
        lri = calculate_lri(scores)

        assert lri == 100.0

    def test_lri_middle_score(self):
        """All 3s should give LRI of 50."""
        scores = {
            "clarity": 3,
            "completeness": 3,
            "conciseness": 3,
            "technical_accuracy": 3,
            "llm_friendliness": 3,
        }
        lri = calculate_lri(scores)

        assert lri == 50.0

    def test_lri_mixed_scores(self):
        """Mixed scores should calculate correct average."""
        scores = {
            "clarity": 4,
            "completeness": 3,
            "conciseness": 5,
            "technical_accuracy": 4,
            "llm_friendliness": 3,
        }
        # Average = (4+3+5+4+3)/5 = 19/5 = 3.8
        # LRI = (3.8 - 1) / 4 * 100 = 2.8/4 * 100 = 70
        lri = calculate_lri(scores)

        assert lri == 70.0

    def test_lri_handles_missing_dimension(self):
        """Should raise ValueError if a dimension is missing."""
        scores = {
            "clarity": 4,
            "completeness": 3,
            # Missing conciseness, technical_accuracy, llm_friendliness
        }

        with pytest.raises(ValueError, match="Missing required dimension"):
            calculate_lri(scores)


class TestLLMEvaluator:
    """Tests for LLMEvaluator class."""

    def test_evaluator_initialization(self):
        """Evaluator should initialize with required parameters."""
        evaluator = LLMEvaluator(api_key="test-key", model="test-model")

        assert evaluator.api_key == "test-key"
        assert evaluator.model == "test-model"

    def test_evaluator_default_parameters(self):
        """Evaluator should have sensible defaults."""
        evaluator = LLMEvaluator(api_key="test-key", model="test-model")

        assert evaluator.max_tokens == 2000
        assert evaluator.max_chunks == 5

    def test_evaluator_requires_api_key(self):
        """Evaluator should raise error if api_key is not provided."""
        with pytest.raises(ValueError, match="api_key"):
            LLMEvaluator(api_key="", model="test-model")

    def test_evaluator_requires_model(self):
        """Evaluator should raise error if model is not provided."""
        with pytest.raises(ValueError, match="model"):
            LLMEvaluator(api_key="test-key", model="")
