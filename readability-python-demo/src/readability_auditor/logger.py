"""Structured logging with status tags."""

from rich.console import Console
from rich.text import Text

console = Console()


def log_found(url: str, file_type: str) -> None:
    """Log when llm.txt/llms.txt is found."""
    tag = Text("[FOUND]", style="bold green")
    console.print(f"{tag} {url}/{file_type}")


def log_not_found(url: str) -> None:
    """Log when neither llm.txt nor llms.txt exists."""
    tag = Text("[NOT FOUND]", style="bold red")
    console.print(f"{tag} {url} — No llm.txt or llms.txt")


def log_scrape(url: str, chars: int) -> None:
    """Log scraping progress."""
    tag = Text("[SCRAPE]", style="bold cyan")
    console.print(f"{tag} {url} → {chars:,} chars")


def log_metrics(metrics_type: str, fre: float, fk: float, ld: float, twr: float) -> None:
    """Log calculated metrics."""
    tag = Text("[METRICS]", style="bold yellow")
    console.print(
        f"{tag} {metrics_type}: FRE={fre:.2f} | FK={fk:.2f} | LD={ld:.1f}% | T/W={twr:.2f}"
    )


def log_error(url: str, error: str) -> None:
    """Log errors."""
    tag = Text("[ERROR]", style="bold red")
    console.print(f"{tag} {url} — {error}")


def log_complete(success: int, failed: int) -> None:
    """Log completion summary."""
    console.print()
    console.print("[bold green]Audit complete![/bold green]")
    console.print(f"  Success: {success}")
    console.print(f"  Failed: {failed}")
