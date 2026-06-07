"""LLM prompt templates and evaluation rubric."""

import json
import re
from typing import Dict


SYSTEM_PROMPT = """You are a senior technical documentation reviewer with expertise in software engineering and linguistics. Your task is to evaluate technical documentation on 5 dimensions using a 1-5 Likert scale.

Evaluation Rules:
- Be objective and consistent. Rate based on the actual text quality, not your personal preference.
- If the text is a code snippet or API reference, evaluate how well it is explained in prose.
- Ignore purely navigational content (menus, breadcrumbs) if present.
- Rate each dimension independently — a text can score high on Clarity but low on Completeness.

Output Format:
Return ONLY a JSON object with integer scores (1-5) for each dimension. No explanation, no markdown formatting."""


def build_evaluation_prompt(text: str, platform_name: str, doc_type: str) -> str:
    """
    Build a user prompt for evaluating technical documentation.

    Args:
        text: The documentation text to evaluate
        platform_name: Name of the platform (e.g., "React", "FastAPI")
        doc_type: Type of document ("human_docs" or "llm.txt")

    Returns:
        Formatted prompt string with text and evaluation rubric
    """
    prompt = f"""## Document to Evaluate
[Platform: {platform_name}]
[Type: {doc_type}]

{text}

## Evaluation Dimensions

### 1. Clarity
Is the text clear, unambiguous, and easy to follow? Are technical terms explained or defined?
- 1: Very confusing, undefined jargon, unclear structure
- 3: Understandable but requires effort, some undefined terms
- 5: Crystal clear, all concepts explained with examples

### 2. Completeness
Does the text cover the topic adequately? Are there missing details or gaps?
- 1: Severely incomplete, missing critical information
- 3: Covers basics but misses some important details
- 5: Comprehensive, covers all relevant aspects thoroughly

### 3. Conciseness
Is the text free of unnecessary verbosity, repetition, or filler?
- 1: Extremely verbose, full of filler and repetition
- 3: Some redundancy but mostly relevant
- 5: Every sentence adds value, no fluff

### 4. Technical Accuracy
Are the technical details, code examples, and explanations correct?
- 1: Contains factual errors or misleading information
- 3: Mostly correct but with minor inaccuracies
- 5: Technically precise, code works, no errors

### 5. LLM-Friendliness
Is the text optimized for machine consumption? Structured, well-formatted, token-efficient?
- 1: Unstructured, poorly formatted, hard to parse
- 3: Decent structure but not optimized for LLMs
- 5: Perfectly structured for LLM ingestion, clear headings, efficient

## Output
Return ONLY this JSON:
{{
  "clarity": 1,
  "completeness": 1,
  "conciseness": 1,
  "technical_accuracy": 1,
  "llm_friendliness": 1
}}"""

    return prompt


def parse_json_response(response: str) -> Dict[str, int]:
    """
    Parse LLM JSON response and extract dimension scores.

    Args:
        response: Raw response text from LLM (may include extra text)

    Returns:
        Dictionary with scores for each dimension

    Raises:
        ValueError: If JSON is invalid, missing dimensions, or scores out of range
    """
    # Try to extract JSON from response - look for JSON object
    json_patterns = [
        r'\{[^{}]*"clarity"[^{}]*\}',  # JSON with clarity field
        r'\{[^{}]*\}',  # Any JSON object
    ]
    
    json_str = None
    for pattern in json_patterns:
        json_match = re.search(pattern, response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            break

    if not json_str:
        raise ValueError(f"Could not parse JSON from response: {response[:200]}")

    try:
        scores = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse JSON: {e}. Raw: {json_str[:200]}")

    # Validate all required dimensions are present
    required_dimensions = [
        "clarity",
        "completeness",
        "conciseness",
        "technical_accuracy",
        "llm_friendliness",
    ]

    for dimension in required_dimensions:
        if dimension not in scores:
            raise ValueError(f"Missing required dimension: {dimension}. Got: {list(scores.keys())}")

        score = scores[dimension]

        # Validate score is within 1-5 range
        if not isinstance(score, (int, float)) or score < 1 or score > 5:
            raise ValueError(
                f"Score must be between 1 and 5 for {dimension}, got {score} (type: {type(score).__name__})"
            )
        
        # Convert float to int if needed
        scores[dimension] = int(score)

    return {dim: scores[dim] for dim in required_dimensions}
