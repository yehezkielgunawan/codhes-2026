# Readability Auditor

A Python CLI tool that automates the analysis of documentation readability, comparing human-centric documentation against machine-optimized LLM text files (`llm.txt` / `llms.txt`).

## Features

- **Automated LLM compliance detection** — Checks if domains publish `llm.txt` or `llms.txt`
- **Linked .txt file aggregation** — Follows `.txt` links in `llms.txt` to fetch full documentation
- **Context7 API fallback** — Uses Context7 API when `llms.txt` not found or `llms-full.txt` missing
- **Deep documentation crawling** — BFS multi-page crawl (configurable depth/pages)
- **Prose extraction** — Automatically strips code blocks, navigation, images, and UI elements from human docs for fair comparison
- **Dual corpus scraping** — Fetches both human docs (HTML) and machine text (plain text)
- **Readability metrics** — Calculates Flesch Reading Ease, Flesch-Kincaid Grade, Lexical Density, and Token-to-Word Ratio
- **LLM-as-a-Judge evaluation** — Evaluates documentation quality using OpenRouter API on 5 dimensions (Clarity, Completeness, Conciseness, Technical Accuracy, LLM-Friendliness)
- **LLM Readability Index (LRI)** — Quantifies LLM evaluation scores on 0-100 scale for comparison with traditional metrics
- **Structured export** — Outputs results to CSV and Markdown formats
- **Progress logging** — Real-time status tags for found/not-found URLs
- **Resumable evaluation** — Caches LLM API responses for fault-tolerant batch processing

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to project directory
cd readability-python-demo

# Dependencies are automatically installed on first run
```

## Usage

### Basic Audit (Traditional Metrics Only)

1. Create a `urls.txt` file with target URLs (one per line):

```
https://fastapi.tiangolo.com
https://docs.pydantic.dev
https://langchain.com
```

2. Run the audit:

```bash
uv run readability-auditor run --input urls.txt --output-dir ./results
```

3. Check the results:
   - `results/results.csv` — Raw data with all metrics
   - `results/report.md` — Formatted summary with comparison tables

### Scrape Single URL

To scrape human documentation from a single URL (useful for fixing missing data):

```bash
uv run readability-auditor scrape https://docs.cursor.com --max-pages 10
```

This will:
- Crawl the documentation site (with JavaScript rendering for SPAs)
- Clean the content (strip code blocks, navigation, images)
- Calculate traditional metrics (FRE, FKGL, LD, T/W)
- Save to `results/raw_texts/{domain}_human.md`

### LLM-as-a-Judge Evaluation

To evaluate documentation quality using an LLM:

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY=sk-or-...

# Run audit with LLM evaluation
uv run readability-auditor run --input urls.txt --output-dir ./results --evaluate-llm

# Or evaluate existing raw_texts (skip scraping)
uv run readability-auditor run --output-dir ./results --evaluate-only
```

Results include:
- `results/llm_evaluation.csv` — LLM scores for each dimension
- `results/llm_cache/` — Cached API responses (resumable)

## CLI Commands

### `run` — Full Audit Pipeline

```bash
uv run readability-auditor run [OPTIONS]

Options:
  -i, --input PATH              Path to URLs file [default: urls.txt]
  -o, --output-dir PATH         Directory to save results [default: ./results]
  -d, --max-depth INT           Max depth for crawling docs (1-5) [default: 2]
  -p, --max-pages INT           Max pages to crawl per URL (1-50) [default: 10]
  --follow-links/--no-follow-links  Follow .txt links in llms.txt [default: follow-links]
  --use-context7/--no-context7  Use Context7 API as fallback [default: use-context7]
  --evaluate-llm/--no-evaluate-llm  Run LLM-as-a-Judge evaluation [default: no-evaluate-llm]
  --evaluate-only               Run LLM evaluation on existing raw_texts (skip scraping)
  --llm-model TEXT              OpenRouter model for LLM evaluation [default: nvidia/nemotron-nano-12b-v2-vl:free]
  --llm-api-key TEXT            OpenRouter API key (or set OPENROUTER_API_KEY env var)
  -v, --verbose                 Enable verbose logging
```

### `scrape` — Single URL Scraping

```bash
uv run readability-auditor scrape URL [OPTIONS]

Arguments:
  URL                           Single URL to scrape [required]

Options:
  -o, --output-dir PATH         Directory to save results [default: ./results]
  -d, --max-depth INT           Max depth for crawling docs (1-5) [default: 2]
  -p, --max-pages INT           Max pages to crawl per URL (1-50) [default: 10]
  --evaluate-llm/--no-evaluate-llm  Run LLM-as-a-Judge evaluation [default: no-evaluate-llm]
  --llm-model TEXT              OpenRouter model for LLM evaluation
  --llm-api-key TEXT            OpenRouter API key (or set OPENROUTER_API_KEY env var)
```

**Use case:** Fix missing human docs for specific platforms without re-running the full pipeline.

**Example:**
```bash
# Scrape Cursor docs only
uv run readability-auditor scrape https://docs.cursor.com --max-pages 10
```

## Context7 API Integration

The tool can use the [Context7 API](https://context7.com) as a fallback when:
- `llms.txt` or `llm.txt` is not found on the domain
- `llms-full.txt` is not referenced in the found `llms.txt`

To use this feature, set your Context7 API token in `.env`:

```bash
CONTEXT7_TOKEN=ctx7sk-your-token-here
```

The token is automatically loaded from the `.env` file when running the CLI.

## OpenRouter API Integration

The tool uses [OpenRouter](https://openrouter.ai) for LLM-as-a-Judge evaluation:

```bash
# Set API key in .env or environment variable
OPENROUTER_API_KEY=sk-or-...
```

**Default model:** `nvidia/nemotron-nano-12b-v2-vl:free` (free tier)

**Evaluation dimensions (1-5 Likert scale):**
1. **Clarity** — Is the documentation clear and unambiguous?
2. **Completeness** — Does it cover the topic adequately?
3. **Conciseness** — Is it free of unnecessary verbosity?
4. **Technical Accuracy** — Are technical details correct?
5. **LLM-Friendliness** — Is it optimized for machine consumption?

**LLM Readability Index (LRI):**
```
LRI = (Average of 5 dimensions - 1) / 4 × 100
```
Maps 1-5 Likert scale to 0-100 for comparison with Flesch Reading Ease.

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **Flesch Reading Ease (FRE)** | Higher = easier to read. 90-100 = very easy, 0-30 = very difficult |
| **Flesch-Kincaid Grade (FK)** | US school grade level needed to understand the text |
| **Lexical Density (LD)** | Percentage of content words (nouns, verbs, adjectives, adverbs) |
| **Token-to-Word Ratio (T/W)** | AI tokenization efficiency. Lower = more efficient for LLMs |
| **LLM Readability Index (LRI)** | LLM evaluation score (0-100) from 5-dimension assessment |

## Research Context

This tool supports academic research on the "Paradox of Readabilities" — the linguistic shift from human-readable to machine-optimized documentation in the AI era.

**Novel contribution:** First study to use LLM-as-a-Judge methodology for technical documentation readability assessment.

## License

MIT
