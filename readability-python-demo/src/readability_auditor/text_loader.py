"""Load raw text files for LLM evaluation."""

from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse


def get_domain_from_url(url: str) -> str:
    """
    Extract domain from URL for file naming.

    Args:
        url: URL to extract domain from

    Returns:
        Domain string (e.g., "react.dev", "docs.github.com")
    """
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    return domain.rstrip("/")


def find_text_pairs(raw_texts_dir: Path) -> Dict[str, Dict[str, Optional[Path]]]:
    """
    Find all text pairs in raw_texts directory.

    Args:
        raw_texts_dir: Path to raw_texts directory

    Returns:
        Dictionary mapping domain to {"human": Path, "machine": Path}
    """
    pairs = {}

    # Find all machine files
    for machine_file in raw_texts_dir.glob("*_machine.txt"):
        domain = machine_file.stem.replace("_machine", "")
        human_file = raw_texts_dir / f"{domain}_human.md"

        pairs[domain] = {
            "machine": machine_file,
            "human": human_file if human_file.exists() else None,
        }

    return pairs


def load_raw_texts(file_path: Optional[Path]) -> Optional[str]:
    """
    Load text content from a file.

    Args:
        file_path: Path to text file, or None

    Returns:
        File contents as string, or None if path is None
    """
    if file_path is None:
        return None

    return file_path.read_text(encoding="utf-8")
