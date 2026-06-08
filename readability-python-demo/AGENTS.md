# AGENTS.md — readability-python-demo

## Commands

```bash
cd readability-python-demo

# Run full audit pipeline
uv run readability-auditor run --input urls.txt --output-dir ./results

# Run with LLM evaluation
uv run readability-auditor run --input urls.txt --output-dir ./results --evaluate-llm

# Run LLM evaluation on existing raw_texts (skip scraping)
uv run readability-auditor run --output-dir ./results --evaluate-only

# Scrape single URL (useful for fixing missing data)
uv run readability-auditor scrape https://docs.cursor.com --max-pages 10

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
| `httpx` | Async HTTP | For llm.txt detection, Context7 API, and OpenRouter API |
| `rich` | Console output | Status tags, progress |

## Context7 API Integration

The tool uses [Context7 API](https://context7.com) as a fallback when `llms.txt` is not found or incomplete.

**API Token:** Set `CONTEXT7_TOKEN` in `.env` file:
```bash
CONTEXT7_TOKEN=ctx7sk-your-token-here
```

**Fallback Logic:**
1. Try `/llm.txt` and `/llms.txt` directly
2. If found, follow linked `.txt` files
3. If `llms-full.txt` not referenced → try Context7 API
4. **Compare lengths**: use Context7 only if it returns MORE content than `llms.txt`
5. If not found at all → try Context7 API as final fallback

**Disable:** Use `--no-context7` flag to skip Context7 API calls.

## OpenRouter API Integration

The tool uses [OpenRouter](https://openrouter.ai) for LLM-as-a-Judge evaluation.

**API Token:** Set `OPENROUTER_API_KEY` in `.env` file or environment:
```bash
OPENROUTER_API_KEY=sk-or-...
```

**Default Model:** `meta-llama/llama-3.2-3b-instruct:free` (free tier)

**Evaluation Dimensions (1-5 Likert scale):**
1. Clarity — Is the documentation clear and unambiguous?
2. Completeness — Does it cover the topic adequately?
3. Conciseness — Is it free of unnecessary verbosity?
4. Technical Accuracy — Are technical details correct?
5. LLM-Friendliness — Is it optimized for machine consumption?

**LLM Readability Index (LRI):**
```
LRI = (Average of 5 dimensions - 1) / 4 × 100
```
Maps 1-5 Likert scale to 0-100 for comparison with Flesch Reading Ease.

**Caching:** API responses cached to `results/llm_cache/{domain}_{doc_type}_{chunk}.json` for resumable batch processing.

**Rate Limiting:** Automatic retry with exponential backoff and `Retry-After` header respect.

## Project Structure

```
readability-python-demo/
├── src/readability_auditor/   # Source code (NOT root)
│   ├── cli.py                 # Typer app, no subcommands
│   ├── llm_detector.py        # Detects llm.txt/llms.txt, follows links, Context7 fallback
│   ├── context7_client.py     # Context7 API client for fallback
│   ├── llm_evaluator.py       # LLM-as-a-Judge evaluation engine
│   ├── llm_prompts.py         # Prompt templates and JSON parsing
│   ├── text_loader.py         # Loads raw texts for evaluate-only mode
│   ├── scraper.py             # Crawl4AI deep crawling
│   ├── text_cleaner.py        # Cleans human docs (strips code blocks, nav, images)
│   ├── metrics.py             # Readability calculations
│   ├── exporter.py            # CSV + Markdown + raw text export
│   ├── logger.py              # Rich console output
│   └── models.py              # AuditResult, Metrics, LLMScores dataclasses
├── tests/                     # pytest tests (50 tests)
├── urls.txt                   # Sample input
├── .env                       # CONTEXT7_TOKEN, OPENROUTER_API_KEY (gitignored)
└── results/                   # Output (gitignored)
    ├── results.csv
    ├── llm_evaluation.csv     # LLM scores (if --evaluate-llm)
    ├── report.md
    ├── llm_cache/             # Cached LLM API responses
    └── raw_texts/             # Scraped content
```

## Gotchas

- **Two commands** — CLI has `run` (full pipeline) and `scrape` (single URL) subcommands
- **Source in `src/`** — Package lives in `src/readability_auditor/`, not root
- **Crawl4AI needs browsers** — Run `uv run playwright install chromium` first
- **JavaScript rendering** — Scraper uses `wait_for` and `delay_before_return_html` for SPAs (e.g., Cursor docs)
- **NLTK auto-downloads** — `stopwords` corpus downloads on first import
- **Raw text export** — Scraped content saves to `results/raw_texts/{domain}_human.md` and `{domain}_machine.txt`
- **Human docs are cleaned** — `text_cleaner.py` strips code blocks, navigation, images, and inline code before metrics calculation. This ensures fair comparison with machine text.
- **LLM evaluation is async** — Uses `httpx.AsyncClient` with rate limiting and retry logic
- **Cache is resumable** — If API fails mid-batch, re-run will skip cached chunks
- **OpenRouter free tier rate limits** — May hit 429 errors; tool auto-retries with backoff
- **Minimum content threshold** — Cleaned content must be >500 chars or scraper tries next URL

## Testing

- Uses `pytest` with `pytest-asyncio` and `pytest-httpx`
- Async tests work out of the box
- Mock HTTP with `httpx_mock` fixture
- 50 tests total (11 original + 39 new for LLM evaluation)

## Environment Variables

Set in `.env` file (gitignored):
```bash
CONTEXT7_TOKEN=ctx7sk-your-token-here
OPENROUTER_API_KEY=sk-or-...
```
