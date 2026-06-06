"""Calculate readability metrics for text corpora."""

import textstat
import tiktoken
from typing import Optional

from .models import Metrics

import nltk
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords


def calculate_metrics(text: str) -> Optional[Metrics]:
    """
    Calculate readability metrics for a given text.

    Returns None if text is empty or too short.
    """
    if not text or len(text.strip()) < 50:
        return None

    words = text.split()
    total_words = len(words)

    if total_words == 0:
        return None

    fre_score = textstat.flesch_reading_ease(text)
    fk_grade = textstat.flesch_kincaid_grade(text)

    stop_words = set(stopwords.words("english"))
    content_words = [w for w in words if w.lower() not in stop_words]
    lexical_density = (len(content_words) / total_words) * 100

    encoding = tiktoken.get_encoding("cl100k_base")
    token_count = len(encoding.encode(text))
    token_ratio = token_count / total_words

    return Metrics(
        flesch_reading_ease=fre_score,
        flesch_kincaid_grade=fk_grade,
        lexical_density=lexical_density,
        token_count=token_count,
        word_count=total_words,
        token_to_word_ratio=token_ratio,
    )
