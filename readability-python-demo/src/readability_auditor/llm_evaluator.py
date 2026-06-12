"""LLM evaluator engine for documentation quality assessment."""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import httpx
import tiktoken

from .llm_prompts import SYSTEM_PROMPT, build_evaluation_prompt, parse_json_response


def chunk_text(text: str, max_tokens: int = 2000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap for LLM evaluation.

    Args:
        text: The text to chunk
        max_tokens: Maximum tokens per chunk
        overlap: Number of overlapping tokens between chunks

    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        return []

    # Ensure overlap is less than max_tokens to avoid infinite loop
    if overlap >= max_tokens:
        overlap = max_tokens // 2

    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        return [text]

    chunks = []
    start = 0
    step = max_tokens - overlap

    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

        start += step

        if end >= len(tokens):
            break

    return chunks


def calculate_lri(scores: Dict[str, int]) -> float:
    """
    Calculate LLM Readability Index from dimension scores.

    Formula: LRI = (Average of 5 dimensions - 1) / 4 * 100

    Args:
        scores: Dictionary with scores for each dimension (1-5)

    Returns:
        LRI score (0-100)

    Raises:
        ValueError: If required dimensions are missing
    """
    required_dimensions = [
        "clarity",
        "completeness",
        "conciseness",
        "technical_accuracy",
        "llm_friendliness",
    ]

    for dimension in required_dimensions:
        if dimension not in scores:
            raise ValueError(f"Missing required dimension: {dimension}")

    average = sum(scores[dim] for dim in required_dimensions) / len(required_dimensions)
    lri = (average - 1) / 4 * 100

    return lri


class LLMEvaluator:
    """Evaluator for documentation quality using LLM-as-a-Judge."""

    def __init__(
        self,
        api_key: str,
        model: str,
        max_tokens: int = 2000,
        max_chunks: int = 5,
        cache_dir: Optional[Path] = None,
    ):
        """
        Initialize LLM evaluator.

        Args:
            api_key: OpenRouter API key
            model: Model identifier (e.g., "nvidia/nemotron-nano-12b-v2-vl:free")
            max_tokens: Maximum tokens per chunk
            max_chunks: Maximum number of chunks to evaluate per document
            cache_dir: Directory for caching API responses
        """
        if not api_key:
            raise ValueError("api_key is required")
        if not model:
            raise ValueError("model is required")

        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.max_chunks = max_chunks
        self.cache_dir = cache_dir or Path("./results/llm_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def evaluate_text(
        self,
        text: str,
        platform_name: str,
        doc_type: str,
        chunk_index: int = 0,
    ) -> Optional[Dict[str, int]]:
        """
        Evaluate a single text chunk using OpenRouter API.

        Args:
            text: Text chunk to evaluate
            platform_name: Name of the platform
            doc_type: Type of document ("human_docs" or "llm.txt")
            chunk_index: Index of the chunk (for caching)

        Returns:
            Dictionary with dimension scores, or None if evaluation fails
        """
        # Check cache first
        cache_file = self.cache_dir / f"{platform_name}_{doc_type}_{chunk_index}.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)

        # Build prompt
        user_prompt = build_evaluation_prompt(text, platform_name, doc_type)

        # Call OpenRouter API with retry logic
        max_retries = 5
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://github.com/yehezkielgunawan/readability-python-demo",
                            "X-OpenRouter-Title": "Readability Auditor",
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": user_prompt},
                            ],
                            "temperature": 0.1,
                        },
                    )
                    
                    # Handle rate limiting specifically
                    if response.status_code == 429:
                        retry_after = int(response.headers.get("Retry-After", 10))
                        print(f"  [WARN] Rate limited. Waiting {retry_after}s before retry...")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    response.raise_for_status()

                    result = response.json()
                    
                    # Check if we got a valid response
                    if "choices" not in result or len(result["choices"]) == 0:
                        raise ValueError(f"No choices in response: {result}")
                    
                    content = result["choices"][0]["message"]["content"]
                    
                    # Log raw response for debugging
                    print(f"  [DEBUG] Raw response: {content[:200]}...")

                    # Parse response
                    scores = parse_json_response(content)

                    # Cache result
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(scores, f, indent=2)

                    return scores

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    retry_after = int(e.response.headers.get("Retry-After", 10))
                    print(f"  [WARN] Rate limited. Waiting {retry_after}s before retry...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"  [WARN] Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        await asyncio.sleep(2 ** attempt)
                    else:
                        print(f"  [ERROR] All retries failed for {platform_name} {doc_type} chunk {chunk_index}")
                        return None
            except Exception as e:
                print(f"  [WARN] Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    # Exponential backoff
                    await asyncio.sleep(2 ** attempt)
                else:
                    print(f"  [ERROR] All retries failed for {platform_name} {doc_type} chunk {chunk_index}")
                    return None

    async def evaluate_document(
        self,
        text: str,
        platform_name: str,
        doc_type: str,
    ) -> Optional[Dict[str, float]]:
        """
        Evaluate a full document by chunking and averaging scores.

        Args:
            text: Full document text
            platform_name: Name of the platform
            doc_type: Type of document ("human_docs" or "llm.txt")

        Returns:
            Dictionary with average scores and LRI, or None if evaluation fails
        """
        chunks = chunk_text(text, self.max_tokens, overlap=200)

        if not chunks:
            return None

        # Limit to max_chunks
        chunks = chunks[: self.max_chunks]

        # Evaluate each chunk
        all_scores = []
        for i, chunk in enumerate(chunks):
            scores = await self.evaluate_text(chunk, platform_name, doc_type, i)
            if scores:
                all_scores.append(scores)
            
            # Add delay between requests to avoid rate limiting
            if i < len(chunks) - 1:
                await asyncio.sleep(2)

        if not all_scores:
            return None

        # Average scores across chunks
        dimensions = ["clarity", "completeness", "conciseness", "technical_accuracy", "llm_friendliness"]
        avg_scores = {dim: sum(s[dim] for s in all_scores) / len(all_scores) for dim in dimensions}

        # Calculate LRI
        avg_scores["overall_lri"] = calculate_lri(avg_scores)

        return avg_scores
