"""Data models for audit results."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Metrics:
    """Readability metrics for a text corpus."""

    flesch_reading_ease: float
    flesch_kincaid_grade: float
    lexical_density: float
    token_count: int
    word_count: int
    token_to_word_ratio: float


@dataclass
class AuditResult:
    """Result of auditing a single URL."""

    base_url: str
    llm_status: str
    llm_file_type: Optional[str] = None
    human_doc_url: Optional[str] = None
    human_text: Optional[str] = None
    machine_text: Optional[str] = None
    human_metrics: Optional[Metrics] = None
    machine_metrics: Optional[Metrics] = None
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
