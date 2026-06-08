"""CLI interface using Typer."""

import asyncio
import os
from pathlib import Path

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import logger
from .exporter import export_results
from .llm_detector import detect_llm_txt
from .llm_evaluator import LLMEvaluator
from .metrics import calculate_metrics
from .models import AuditResult, LLMScores
from .scraper import scrape_human_documentation
from .text_loader import find_text_pairs, load_raw_texts

app = typer.Typer(help="Audit documentation readability")


@app.command()
def scrape(
    url: str = typer.Argument(..., help="Single URL to scrape"),
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
    evaluate_llm: bool = typer.Option(
        False,
        "--evaluate-llm/--no-evaluate-llm",
        help="Run LLM-as-a-Judge evaluation on scraped content",
    ),
    llm_model: str = typer.Option(
        "meta-llama/llama-3.2-3b-instruct:free",
        "--llm-model",
        help="OpenRouter model for LLM evaluation",
    ),
    llm_api_key: str = typer.Option(
        "",
        "--llm-api-key",
        help="OpenRouter API key (or set OPENROUTER_API_KEY env var)",
    ),
) -> None:
    """Scrape human documentation from a single URL."""
    typer.echo(f"Scraping: {url}")
    typer.echo(f"Config: max_depth={max_depth}, max_pages={max_pages}")
    typer.echo()

    result = asyncio.run(_scrape_single_url(
        url,
        max_depth,
        max_pages,
        evaluate_llm,
        llm_model,
        llm_api_key,
        output_dir,
    ))

    # Export single result
    raw_texts_dir = output_dir / "raw_texts"
    raw_texts_dir.mkdir(parents=True, exist_ok=True)

    if result.human_text:
        from .text_loader import get_domain_from_url
        domain = get_domain_from_url(url)
        human_path = raw_texts_dir / f"{domain}_human.md"
        human_path.write_text(result.human_text, encoding="utf-8")
        typer.echo(f"\n✓ Saved human docs to: {human_path}")

        if result.human_metrics:
            logger.log_metrics(
                "Human",
                result.human_metrics.flesch_reading_ease,
                result.human_metrics.flesch_kincaid_grade,
                result.human_metrics.lexical_density,
                result.human_metrics.token_to_word_ratio,
            )

        if result.human_llm_scores:
            typer.echo(f"Human LRI: {result.human_llm_scores.overall_lri:.2f}")
    else:
        typer.echo("\n✗ Failed to scrape human documentation", err=True)


async def _scrape_single_url(
    url: str,
    max_depth: int,
    max_pages: int,
    evaluate_llm: bool,
    llm_model: str,
    llm_api_key: str,
    output_dir: Path,
) -> AuditResult:
    """Scrape a single URL."""
    result = AuditResult(base_url=url, llm_status="NOT_FOUND")

    # Scrape human documentation
    human_text = await scrape_human_documentation(
        url,
        max_depth=max_depth,
        max_pages=max_pages,
    )

    if human_text:
        result.human_text = human_text
        result.human_metrics = calculate_metrics(human_text)
        typer.echo(f"✓ Scraped {len(human_text):,} characters")
    else:
        typer.echo("✗ No content scraped - pages may be empty or blocked", err=True)

    # Run LLM evaluation if enabled
    if evaluate_llm and human_text:
        api_key = llm_api_key or os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            typer.echo("Warning: OPENROUTER_API_KEY not set. LLM evaluation skipped.", err=True)
        else:
            evaluator = LLMEvaluator(
                api_key=api_key,
                model=llm_model,
                cache_dir=output_dir / "llm_cache",
            )

            typer.echo("Running LLM evaluation...")
            human_scores = await evaluator.evaluate_document(
                human_text,
                platform_name=url,
                doc_type="human_docs",
            )
            if human_scores:
                result.human_llm_scores = human_scores

    return result


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
    evaluate_llm: bool = typer.Option(
        False,
        "--evaluate-llm/--no-evaluate-llm",
        help="Run LLM-as-a-Judge evaluation on documentation",
    ),
    evaluate_only: bool = typer.Option(
        False,
        "--evaluate-only",
        help="Run LLM evaluation only on existing raw_texts (skip scraping)",
    ),
    llm_model: str = typer.Option(
        "nvidia/nemotron-nano-12b-v2-vl:free",
        "--llm-model",
        help="OpenRouter model for LLM evaluation",
    ),
    llm_api_key: str = typer.Option(
        "",
        "--llm-api-key",
        help="OpenRouter API key (or set OPENROUTER_API_KEY env var)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
) -> None:
    """Run full audit pipeline on URLs from input file."""
    # Handle evaluate-only mode
    if evaluate_only:
        typer.echo("Running LLM evaluation on existing raw_texts...")
        results = asyncio.run(
            _evaluate_from_raw_texts(
                output_dir,
                llm_model,
                llm_api_key,
            )
        )
        export_results(results, output_dir)

        success = sum(1 for r in results if r.llm_status == "FOUND")
        failed = len(results) - success
        logger.log_complete(success, failed)
        typer.echo(f"\nResults saved to: {output_dir}/")
        return

    with open(input, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        typer.echo("No URLs found in input file.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Starting audit for {len(urls)} URLs...")
    typer.echo(
        f"Crawl config: max_depth={max_depth}, max_pages={max_pages}, follow_links={follow_links}, context7={use_context7}"
    )

    if evaluate_llm:
        typer.echo(f"LLM evaluation: enabled (model={llm_model})")

    typer.echo()

    results = asyncio.run(
        _audit_urls(
            urls,
            max_depth,
            max_pages,
            follow_links,
            use_context7,
            evaluate_llm,
            llm_model,
            llm_api_key,
            output_dir,
        )
    )

    export_results(results, output_dir)

    success = sum(1 for r in results if r.llm_status == "FOUND")
    failed = len(results) - success
    logger.log_complete(success, failed)
    typer.echo(f"\nResults saved to: {output_dir}/")


async def _audit_urls(
    urls: list[str],
    max_depth: int,
    max_pages: int,
    follow_links: bool,
    use_context7: bool,
    evaluate_llm: bool,
    llm_model: str,
    llm_api_key: str,
    output_dir: Path,
) -> list[AuditResult]:
    """Process all URLs asynchronously."""
    results = []

    # Initialize LLM evaluator if needed
    evaluator = None
    if evaluate_llm:
        api_key = llm_api_key or os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            typer.echo(
                "Warning: OPENROUTER_API_KEY not set. LLM evaluation will be skipped.",
                err=True,
            )
        else:
            evaluator = LLMEvaluator(
                api_key=api_key,
                model=llm_model,
                cache_dir=output_dir / "llm_cache",
            )

    for url in urls:
        try:
            result = await _audit_single_url(
                url,
                max_depth,
                max_pages,
                follow_links,
                use_context7,
                evaluator,
            )
            results.append(result)
        except Exception as e:
            typer.echo(f"[ERROR] Failed to audit {url}: {e}", err=True)
            # Create a failed result to maintain data integrity
            failed_result = AuditResult(
                base_url=url,
                llm_status="ERROR",
                error=str(e),
            )
            results.append(failed_result)

    return results


async def _audit_single_url(
    base_url: str,
    max_depth: int,
    max_pages: int,
    follow_links: bool,
    use_context7: bool,
    evaluator: LLMEvaluator | None,
) -> AuditResult:
    """Audit a single URL."""
    result = AuditResult(base_url=base_url, llm_status="NOT_FOUND")

    machine_text, file_type = await detect_llm_txt(
        base_url,
        follow_links=follow_links,
        use_context7_fallback=use_context7,
    )

    if not machine_text:
        return result

    result.llm_status = "FOUND"
    result.llm_file_type = file_type
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

    # Scrape human documentation
    human_text = await scrape_human_documentation(
        base_url,
        max_depth=max_depth,
        max_pages=max_pages,
    )

    if human_text:
        result.human_text = human_text
        result.human_metrics = calculate_metrics(human_text)

        if result.human_metrics:
            logger.log_metrics(
                "Human",
                result.human_metrics.flesch_reading_ease,
                result.human_metrics.flesch_kincaid_grade,
                result.human_metrics.lexical_density,
                result.human_metrics.token_to_word_ratio,
            )

    # Run LLM evaluation if enabled
    if evaluator:
        typer.echo(f"  Running LLM evaluation...")
        
        # Evaluate machine text
        if result.machine_text:
            machine_scores = await evaluator.evaluate_document(
                result.machine_text,
                platform_name=base_url,
                doc_type="llm.txt",
            )
            if machine_scores:
                result.machine_llm_scores = machine_scores
                typer.echo(f"  Machine LRI: {machine_scores.overall_lri:.2f}")

        # Evaluate human text
        if result.human_text:
            human_scores = await evaluator.evaluate_document(
                result.human_text,
                platform_name=base_url,
                doc_type="human_docs",
            )
            if human_scores:
                result.human_llm_scores = human_scores
                typer.echo(f"  Human LRI: {human_scores.overall_lri:.2f}")

    return result


async def _evaluate_from_raw_texts(
    output_dir: Path,
    llm_model: str,
    llm_api_key: str,
) -> list[AuditResult]:
    """Run LLM evaluation on existing raw_texts files."""
    raw_texts_dir = output_dir / "raw_texts"

    if not raw_texts_dir.exists():
        typer.echo(f"Error: raw_texts directory not found at {raw_texts_dir}", err=True)
        raise typer.Exit(1)

    # Initialize LLM evaluator
    api_key = llm_api_key or os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        typer.echo("Error: OPENROUTER_API_KEY not set.", err=True)
        raise typer.Exit(1)

    evaluator = LLMEvaluator(
        api_key=api_key,
        model=llm_model,
        cache_dir=output_dir / "llm_cache",
    )

    typer.echo(f"LLM model: {llm_model}")
    typer.echo(f"Reading from: {raw_texts_dir}")
    typer.echo()

    # Find all text pairs
    pairs = find_text_pairs(raw_texts_dir)

    if not pairs:
        typer.echo("Error: No text files found in raw_texts directory.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Found {len(pairs)} platforms to evaluate")
    typer.echo()

    results = []

    for domain, paths in pairs.items():
        typer.echo(f"[EVALUATE] {domain}")

        # Load texts
        machine_text = load_raw_texts(paths["machine"])
        human_text = load_raw_texts(paths["human"])

        if not machine_text:
            typer.echo(f"  Skipping: no machine text")
            continue

        # Create result
        result = AuditResult(
            base_url=f"https://{domain}",
            llm_status="FOUND",
            llm_file_type="llms.txt",
            machine_text=machine_text,
            machine_metrics=calculate_metrics(machine_text),
        )

        if human_text:
            result.human_text = human_text
            result.human_metrics = calculate_metrics(human_text)

        # Log metrics
        if result.machine_metrics:
            logger.log_metrics(
                "Machine",
                result.machine_metrics.flesch_reading_ease,
                result.machine_metrics.flesch_kincaid_grade,
                result.machine_metrics.lexical_density,
                result.machine_metrics.token_to_word_ratio,
            )

        if result.human_metrics:
            logger.log_metrics(
                "Human",
                result.human_metrics.flesch_reading_ease,
                result.human_metrics.flesch_kincaid_grade,
                result.human_metrics.lexical_density,
                result.human_metrics.token_to_word_ratio,
            )

        # Run LLM evaluation
        typer.echo(f"  Evaluating with LLM...")

        # Evaluate machine text
        machine_scores = await evaluator.evaluate_document(
            machine_text,
            domain,
            "llm.txt",
        )
        if machine_scores:
            result.machine_llm_scores = LLMScores(**machine_scores)
            typer.echo(f"  Machine LRI: {machine_scores['overall_lri']:.1f}")

        # Evaluate human text
        if human_text:
            human_scores = await evaluator.evaluate_document(
                human_text,
                domain,
                "human_docs",
            )
            if human_scores:
                result.human_llm_scores = LLMScores(**human_scores)
                typer.echo(f"  Human LRI: {human_scores['overall_lri']:.1f}")

        results.append(result)
        typer.echo()

    return results

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

    # Run LLM evaluation if enabled
    if evaluator and result.machine_text:
        typer.echo(f"  Evaluating with LLM...")

        # Evaluate machine text (llm.txt)
        machine_scores = await evaluator.evaluate_document(
            result.machine_text,
            base_url,
            "llm.txt",
        )
        if machine_scores:
            result.machine_llm_scores = LLMScores(**machine_scores)
            typer.echo(f"  Machine LRI: {machine_scores['overall_lri']:.1f}")

        # Evaluate human text
        if result.human_text:
            human_scores = await evaluator.evaluate_document(
                result.human_text,
                base_url,
                "human_docs",
            )
            if human_scores:
                result.human_llm_scores = LLMScores(**human_scores)
                typer.echo(f"  Human LRI: {human_scores['overall_lri']:.1f}")

    return result
