"""Export audit results to CSV and Markdown."""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

from .models import AuditResult


def export_results(results: List[AuditResult], output_dir: Path) -> None:
    """Export results to CSV and Markdown files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    _export_csv(results, output_dir / "results.csv")
    _export_markdown(results, output_dir / "report.md")


def _export_csv(results: List[AuditResult], filepath: Path) -> None:
    """Export results to CSV."""
    fieldnames = [
        "base_url",
        "llm_file_type",
        "llm_status",
        "human_doc_url",
        "human_fre",
        "human_fk",
        "human_ld",
        "human_twr",
        "machine_fre",
        "machine_fk",
        "machine_ld",
        "machine_twr",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = {
                "base_url": result.base_url,
                "llm_file_type": result.llm_file_type or "",
                "llm_status": result.llm_status,
                "human_doc_url": result.human_doc_url or "",
                "human_fre": f"{result.human_metrics.flesch_reading_ease:.2f}" if result.human_metrics else "",
                "human_fk": f"{result.human_metrics.flesch_kincaid_grade:.2f}" if result.human_metrics else "",
                "human_ld": f"{result.human_metrics.lexical_density:.2f}" if result.human_metrics else "",
                "human_twr": f"{result.human_metrics.token_to_word_ratio:.2f}" if result.human_metrics else "",
                "machine_fre": f"{result.machine_metrics.flesch_reading_ease:.2f}" if result.machine_metrics else "",
                "machine_fk": f"{result.machine_metrics.flesch_kincaid_grade:.2f}" if result.machine_metrics else "",
                "machine_ld": f"{result.machine_metrics.lexical_density:.2f}" if result.machine_metrics else "",
                "machine_twr": f"{result.machine_metrics.token_to_word_ratio:.2f}" if result.machine_metrics else "",
            }
            writer.writerow(row)


def _export_markdown(results: List[AuditResult], filepath: Path) -> None:
    """Export results to Markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = len(results)
    found = sum(1 for r in results if r.llm_status == "FOUND")
    not_found = total - found

    lines = [
        "# Readability Audit Report",
        f"Generated: {timestamp}",
        "",
        "## Summary",
        f"- Total URLs: {total}",
        f"- LLM Compliant: {found}",
        f"- Non-Compliant: {not_found}",
        "",
        "## Detailed Results",
        "",
        "| Platform | LLM File | Human FRE | Machine FRE | Δ FRE | Human LD | Machine LD |",
        "|----------|----------|-----------|-------------|-------|----------|------------|",
    ]

    for result in results:
        if result.llm_status == "FOUND" and result.human_metrics and result.machine_metrics:
            delta = result.machine_metrics.flesch_reading_ease - result.human_metrics.flesch_reading_ease
            lines.append(
                f"| {result.base_url} | {result.llm_file_type} | "
                f"{result.human_metrics.flesch_reading_ease:.2f} | "
                f"{result.machine_metrics.flesch_reading_ease:.2f} | "
                f"{delta:+.2f} | "
                f"{result.human_metrics.lexical_density:.1f}% | "
                f"{result.machine_metrics.lexical_density:.1f}% |"
            )

    lines.append("")
    lines.append("## Non-Compliant Platforms")

    for result in results:
        if result.llm_status == "NOT_FOUND":
            lines.append(f"- {result.base_url}")

    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
