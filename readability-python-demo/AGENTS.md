# AGENTS.md — readability-python-demo

## Commands

```bash
cd readability-python-demo

# Run CLI
uv run readability-auditor --input urls.txt --output-dir ./results

# Run tests
uv run pytest tests/ -v

# Run single test
uv run pytest tests/test_metrics.py -v

# Install Playwright browsers (required for Crawl4AI)
uv run playwright install chromium

# Add dependency
uv add <package>

# Add dev dependency
uv add --dev <package>
```

## Key Libraries (Prioritize These)

| Library | Purpose | Notes |
|---------|---------|-------|
| `typer` | CLI framework | Entry point: `readability_auditor.cli:app` |
| `crawl4ai` | Web scraping | Uses `AsyncWebCrawler`, `BFSDeepCrawlStrategy` |
| `textstat` | Readability metrics | `flesch_reading_ease()`, `flesch_kincaid_grade()` |
| `tiktoken` | Token counting | Uses `cl100k_base` encoding |
| `nltk` | Stopwords | Auto-downloads on first import |
| `httpx` | Async HTTP | For llm.txt detection |
| `rich` | Console output | Status tags, progress |

## Project Structure

```
readability-python-demo/
├── src/readability_auditor/   # Source code (NOT root)
│   ├── cli.py                 # Typer app, no subcommands
│   ├── llm_detector.py        # Detects llm.txt/llms.txt, follows links
│   ├── scraper.py             # Crawl4AI deep crawling
│   ├── metrics.py             # Readability calculations
│   ├── exporter.py            # CSV + Markdown + raw text export
│   ├── logger.py              # Rich console output
│   └── models.py              # AuditResult, Metrics dataclasses
├── tests/                     # pytest tests
├── urls.txt                   # Sample input
└── results/                   # Output (gitignored)
    ├── results.csv
    ├── report.md
    └── raw_texts/             # Scraped content
```

## Gotchas

- **No `run` subcommand** — CLI is `uv run readability-auditor --input ...` (not `run --input`)
- **Source in `src/`** — Package lives in `src/readability_auditor/`, not root
- **Crawl4AI needs browsers** — Run `uv run playwright install chromium` first
- **NLTK auto-downloads** — `stopwords` corpus downloads on first import
- **Raw text export** — Scraped content saves to `results/raw_texts/{domain}_human.md` and `{domain}_machine.txt`

## Testing

- Uses `pytest` with `pytest-asyncio` and `pytest-httpx`
- Async tests work out of the box
- Mock HTTP with `httpx_mock` fixture
