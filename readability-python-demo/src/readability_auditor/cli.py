"""CLI interface using Typer."""

import asyncio
from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import logger
from .exporter import export_results
from .llm_detector import detect_llm_txt
from .metrics import calculate_metrics
from .models import AuditResult
from .scraper import scrape_human_documentation

app = typer.Typer(help="Audit documentation readability")


@app.command()
def run(
    input: Path = typer.Option(
        "urls.txt",
        "--input",
        "-i",
        help="Path to URLs file (one URL per line)",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_dir: Path = typer.Option(
        "./results",
        "--output-dir",
        "-o",
        help="Directory to save results",
    ),
    max_depth: int = typer.Option(
        2,
        "--max-depth",
        "-d",
        help="Maximum depth for crawling documentation pages",
        min=1,
        max=5,
    ),
    max_pages: int = typer.Option(
        10,
        "--max-pages",
        "-p",
        help="Maximum number of pages to crawl per URL",
        min=1,
        max=50,
    ),
    follow_links: bool = typer.Option(
        True,
        "--follow-links/--no-follow-links",
        help="Follow .txt links in llms.txt to fetch additional content",
    ),
    use_context7: bool = typer.Option(
        True,
        "--use-context7/--no-context7",
        help="Use Context7 API as fallback when llms.txt not found",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
) -> None:
    """Run full audit pipeline on URLs from input file."""
    with open(input, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        typer.echo("No URLs found in input file.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Starting audit for {len(urls)} URLs...")
    typer.echo(f"Crawl config: max_depth={max_depth}, max_pages={max_pages}, follow_links={follow_links}, context7={use_context7}")
    typer.echo()

    results = asyncio.run(_audit_urls(urls, max_depth, max_pages, follow_links, use_context7))

    export_results(results, output_dir)

    success = sum(1 for r in results if r.llm_status == "FOUND")
    failed = len(results) - success
    logger.log_complete(success, failed)
    typer.echo(f"\nResults saved to: {output_dir}/")


async def _audit_urls(urls: list[str], max_depth: int, max_pages: int, follow_links: bool, use_context7: bool) -> list[AuditResult]:
    """Process all URLs asynchronously."""
    results = []

    for url in urls:
        result = await _audit_single_url(url, max_depth, max_pages, follow_links, use_context7)
        results.append(result)

    return results


async def _audit_single_url(base_url: str, max_depth: int, max_pages: int, follow_links: bool, use_context7: bool) -> AuditResult:
    """Audit a single URL."""
    result = AuditResult(base_url=base_url, llm_status="NOT_FOUND")

    machine_text, file_type = await detect_llm_txt(
        base_url, 
        follow_links=follow_links,
        use_context7_fallback=use_context7,
    )

    if not machine_text:
        return result

    result.llm_file_type = file_type
    result.llm_status = "FOUND"
    result.machine_text = machine_text
    result.machine_metrics = calculate_metrics(machine_text)

    if result.machine_metrics:
        logger.log_metrics(
            "Machine",
            result.machine_metrics.flesch_reading_ease,
            result.machine_metrics.flesch_kincaid_grade,
            result.machine_metrics.lexical_density,
            result.machine_metrics.token_to_word_ratio,
        )

    human_text = await scrape_human_documentation(base_url, max_depth, max_pages)

    if human_text:
        result.human_text = human_text
        result.human_doc_url = f"{base_url.rstrip('/')}/docs"
        result.human_metrics = calculate_metrics(human_text)

        if result.human_metrics:
            logger.log_metrics(
                "Human",
                result.human_metrics.flesch_reading_ease,
                result.human_metrics.flesch_kincaid_grade,
                result.human_metrics.lexical_density,
                result.human_metrics.token_to_word_ratio,
            )

    return result
