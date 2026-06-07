"""Export audit results to CSV and Markdown."""

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List
from urllib.parse import urlparse

from .models import AuditResult


def export_results(results: List[AuditResult], output_dir: Path) -> None:
    """Export results to CSV, Markdown, and raw text files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    _export_csv(results, output_dir / "results.csv")
    _export_markdown(results, output_dir / "report.md")
    _export_raw_texts(results, output_dir / "raw_texts")
    
    # Export LLM evaluation results if available
    has_llm_scores = any(r.human_llm_scores or r.machine_llm_scores for r in results)
    if has_llm_scores:
        _export_llm_csv(results, output_dir / "llm_evaluation.csv")


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
        "human_lri",
        "machine_fre",
        "machine_fk",
        "machine_ld",
        "machine_twr",
        "machine_lri",
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
                "human_lri": f"{result.human_llm_scores.overall_lri:.2f}" if result.human_llm_scores else "",
                "machine_fre": f"{result.machine_metrics.flesch_reading_ease:.2f}" if result.machine_metrics else "",
                "machine_fk": f"{result.machine_metrics.flesch_kincaid_grade:.2f}" if result.machine_metrics else "",
                "machine_ld": f"{result.machine_metrics.lexical_density:.2f}" if result.machine_metrics else "",
                "machine_twr": f"{result.machine_metrics.token_to_word_ratio:.2f}" if result.machine_metrics else "",
                "machine_lri": f"{result.machine_llm_scores.overall_lri:.2f}" if result.machine_llm_scores else "",
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

    # Add LLM evaluation section if available
    has_llm_scores = any(r.human_llm_scores or r.machine_llm_scores for r in results)
    if has_llm_scores:
        lines.append("")
        lines.append("## LLM-as-a-Judge Evaluation")
        lines.append("")
        lines.append("| Platform | Doc Type | Clarity | Completeness | Conciseness | Tech Acc | LLM-Friendly | LRI |")
        lines.append("|----------|----------|---------|--------------|-------------|----------|--------------|-----|")

        for result in results:
            if result.llm_status != "FOUND":
                continue

            if result.human_llm_scores:
                lines.append(
                    f"| {result.base_url} | human_docs | "
                    f"{result.human_llm_scores.clarity:.1f} | "
                    f"{result.human_llm_scores.completeness:.1f} | "
                    f"{result.human_llm_scores.conciseness:.1f} | "
                    f"{result.human_llm_scores.technical_accuracy:.1f} | "
                    f"{result.human_llm_scores.llm_friendliness:.1f} | "
                    f"{result.human_llm_scores.overall_lri:.1f} |"
                )

            if result.machine_llm_scores:
                lines.append(
                    f"| {result.base_url} | llm.txt | "
                    f"{result.machine_llm_scores.clarity:.1f} | "
                    f"{result.machine_llm_scores.completeness:.1f} | "
                    f"{result.machine_llm_scores.conciseness:.1f} | "
                    f"{result.machine_llm_scores.technical_accuracy:.1f} | "
                    f"{result.machine_llm_scores.llm_friendliness:.1f} | "
                    f"{result.machine_llm_scores.overall_lri:.1f} |"
                )

    lines.append("")
    lines.append("## Non-Compliant Platforms")

    for result in results:
        if result.llm_status == "NOT_FOUND":
            lines.append(f"- {result.base_url}")

    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _sanitize_domain(url: str) -> str:
    """Convert URL to safe filename."""
    domain = urlparse(url).netloc or url
    return re.sub(r"[^\w\-.]", "_", domain)


def _export_raw_texts(results: List[AuditResult], output_dir: Path) -> None:
    """Export raw scraped texts to individual files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for result in results:
        if result.llm_status != "FOUND":
            continue

        domain = _sanitize_domain(result.base_url)

        if result.machine_text:
            machine_path = output_dir / f"{domain}_machine.txt"
            machine_path.write_text(result.machine_text, encoding="utf-8")

        if result.human_text:
            human_path = output_dir / f"{domain}_human.md"
            human_path.write_text(result.human_text, encoding="utf-8")


def _export_llm_csv(results: List[AuditResult], filepath: Path) -> None:
    """Export LLM evaluation scores to separate CSV."""
    fieldnames = [
        "base_url",
        "doc_type",
        "clarity",
        "completeness",
        "conciseness",
        "technical_accuracy",
        "llm_friendliness",
        "overall_lri",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            if result.llm_status != "FOUND":
                continue

            # Export human LLM scores
            if result.human_llm_scores:
                row = {
                    "base_url": result.base_url,
                    "doc_type": "human_docs",
                    "clarity": f"{result.human_llm_scores.clarity:.2f}",
                    "completeness": f"{result.human_llm_scores.completeness:.2f}",
                    "conciseness": f"{result.human_llm_scores.conciseness:.2f}",
                    "technical_accuracy": f"{result.human_llm_scores.technical_accuracy:.2f}",
                    "llm_friendliness": f"{result.human_llm_scores.llm_friendliness:.2f}",
                    "overall_lri": f"{result.human_llm_scores.overall_lri:.2f}",
                }
                writer.writerow(row)

            # Export machine LLM scores
            if result.machine_llm_scores:
                row = {
                    "base_url": result.base_url,
                    "doc_type": "llm.txt",
                    "clarity": f"{result.machine_llm_scores.clarity:.2f}",
                    "completeness": f"{result.machine_llm_scores.completeness:.2f}",
                    "conciseness": f"{result.machine_llm_scores.conciseness:.2f}",
                    "technical_accuracy": f"{result.machine_llm_scores.technical_accuracy:.2f}",
                    "llm_friendliness": f"{result.machine_llm_scores.llm_friendliness:.2f}",
                    "overall_lri": f"{result.machine_llm_scores.overall_lri:.2f}",
                }
                writer.writerow(row)
