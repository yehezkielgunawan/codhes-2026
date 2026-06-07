"""Tests for LLM prompt generation and JSON parsing."""

import pytest
from readability_auditor.llm_prompts import (
    build_evaluation_prompt,
    parse_json_response,
    SYSTEM_PROMPT,
)


class TestBuildEvaluationPrompt:
    """Tests for building evaluation prompts."""

    def test_prompt_includes_all_five_dimensions(self):
        """Prompt must include clarity, completeness, conciseness, technical_accuracy, llm_friendliness."""
        text = "Sample documentation text for evaluation."
        prompt = build_evaluation_prompt(text, "React", "human_docs")

        assert "Clarity" in prompt
        assert "Completeness" in prompt
        assert "Conciseness" in prompt
        assert "Technical Accuracy" in prompt
        assert "LLM-Friendliness" in prompt

    def test_prompt_includes_platform_name(self):
        """Prompt should identify the platform being evaluated."""
        text = "Sample text"
        prompt = build_evaluation_prompt(text, "React", "human_docs")

        assert "React" in prompt

    def test_prompt_includes_document_type(self):
        """Prompt should identify whether it's human docs or llm.txt."""
        text = "Sample text"
        prompt_human = build_evaluation_prompt(text, "React", "human_docs")
        prompt_llm = build_evaluation_prompt(text, "React", "llm.txt")

        assert "human_docs" in prompt_human
        assert "llm.txt" in prompt_llm

    def test_prompt_includes_text_content(self):
        """Prompt must include the actual text to be evaluated."""
        text = "This is the documentation text we want to evaluate."
        prompt = build_evaluation_prompt(text, "React", "human_docs")

        assert text in prompt

    def test_prompt_requests_json_output(self):
        """Prompt must explicitly request JSON format output."""
        text = "Sample text"
        prompt = build_evaluation_prompt(text, "React", "human_docs")

        assert "JSON" in prompt
        assert "clarity" in prompt
        assert "completeness" in prompt
        assert "conciseness" in prompt
        assert "technical_accuracy" in prompt
        assert "llm_friendliness" in prompt


class TestParseJsonResponse:
    """Tests for parsing LLM JSON responses."""

    def test_parse_valid_json_response(self):
        """Should extract all 5 dimension scores from valid JSON."""
        response = """
        {
            "clarity": 4,
            "completeness": 3,
            "conciseness": 5,
            "technical_accuracy": 4,
            "llm_friendliness": 3
        }
        """
        scores = parse_json_response(response)

        assert scores["clarity"] == 4
        assert scores["completeness"] == 3
        assert scores["conciseness"] == 5
        assert scores["technical_accuracy"] == 4
        assert scores["llm_friendliness"] == 3

    def test_parse_json_with_extra_text(self):
        """Should extract JSON even if LLM adds explanatory text."""
        response = """
        Here are my evaluation scores:
        {
            "clarity": 4,
            "completeness": 3,
            "conciseness": 5,
            "technical_accuracy": 4,
            "llm_friendliness": 3
        }
        Hope this helps!
        """
        scores = parse_json_response(response)

        assert scores["clarity"] == 4
        assert scores["completeness"] == 3

    def test_parse_json_with_markdown_code_block(self):
        """Should extract JSON from markdown code blocks."""
        response = """
        ```json
        {
            "clarity": 4,
            "completeness": 3,
            "conciseness": 5,
            "technical_accuracy": 4,
            "llm_friendliness": 3
        }
        ```
        """
        scores = parse_json_response(response)

        assert scores["clarity"] == 4

    def test_raises_error_on_missing_dimension(self):
        """Should raise ValueError if any dimension is missing."""
        response = """
        {
            "clarity": 4,
            "completeness": 3
        }
        """
        with pytest.raises(ValueError, match="Missing required dimension"):
            parse_json_response(response)

    def test_raises_error_on_invalid_json(self):
        """Should raise ValueError if response is not valid JSON."""
        response = "This is not JSON at all"
        with pytest.raises(ValueError, match="Could not parse JSON"):
            parse_json_response(response)

    def test_raises_error_on_out_of_range_scores(self):
        """Should raise ValueError if scores are outside 1-5 range."""
        response = """
        {
            "clarity": 6,
            "completeness": 3,
            "conciseness": 5,
            "technical_accuracy": 4,
            "llm_friendliness": 3
        }
        """
        with pytest.raises(ValueError, match="Score must be between 1 and 5"):
            parse_json_response(response)

    def test_raises_error_on_zero_score(self):
        """Should raise ValueError if any score is 0."""
        response = """
        {
            "clarity": 0,
            "completeness": 3,
            "conciseness": 5,
            "technical_accuracy": 4,
            "llm_friendliness": 3
        }
        """
        with pytest.raises(ValueError, match="Score must be between 1 and 5"):
            parse_json_response(response)


class TestSystemPrompt:
    """Tests for the system prompt constant."""

    def test_system_prompt_exists(self):
        """System prompt should be defined as a constant."""
        assert SYSTEM_PROMPT is not None
        assert len(SYSTEM_PROMPT) > 0

    def test_system_prompt_includes_role(self):
        """System prompt should define the LLM's role."""
        assert "technical documentation" in SYSTEM_PROMPT.lower() or "reviewer" in SYSTEM_PROMPT.lower()

    def test_system_prompt_includes_output_format(self):
        """System prompt should specify JSON output format."""
        assert "JSON" in SYSTEM_PROMPT
