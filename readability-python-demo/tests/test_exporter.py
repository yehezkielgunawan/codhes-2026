"""Tests for the exporter module."""

from datetime import datetime
from pathlib import Path
import tempfile

from readability_auditor.exporter import export_results
from readability_auditor.models import AuditResult, Metrics


def test_export_results_creates_files():
    """Test that export creates both CSV and Markdown files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        results = [
            AuditResult(
                base_url="https://example.com",
                llm_file_type="llm.txt",
                llm_status="FOUND",
                human_doc_url="https://example.com/docs",
                human_text="Sample human text " * 50,
                machine_text="Sample machine text " * 50,
                human_metrics=Metrics(
                    flesch_reading_ease=60.0,
                    flesch_kincaid_grade=9.0,
                    lexical_density=45.0,
                    token_count=100,
                    word_count=80,
                    token_to_word_ratio=1.25,
                ),
                machine_metrics=Metrics(
                    flesch_reading_ease=30.0,
                    flesch_kincaid_grade=15.0,
                    lexical_density=80.0,
                    token_count=90,
                    word_count=85,
                    token_to_word_ratio=1.05,
                ),
                timestamp=datetime.now(),
            )
        ]

        output_dir = Path(tmpdir)
        export_results(results, output_dir)

        assert (output_dir / "results.csv").exists()
        assert (output_dir / "report.md").exists()
