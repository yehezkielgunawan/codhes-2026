# Readability Auditor

A Python CLI tool that automates the analysis of documentation readability, comparing human-centric documentation against machine-optimized LLM text files (`llm.txt` / `llms.txt`).

## Features

- **Automated LLM compliance detection** — Checks if domains publish `llm.txt` or `llms.txt`
- **Linked .txt file aggregation** — Follows `.txt` links in `llms.txt` to fetch full documentation
- **Context7 API fallback** — Uses Context7 API when `llms.txt` not found or `llms-full.txt` missing
- **Deep documentation crawling** — BFS multi-page crawl (configurable depth/pages)
- **Dual corpus scraping** — Fetches both human docs (HTML) and machine text (plain text)
- **Readability metrics** — Calculates Flesch Reading Ease, Flesch-Kincaid Grade, Lexical Density, and Token-to-Word Ratio
- **Structured export** — Outputs results to CSV and Markdown formats
- **Progress logging** — Real-time status tags for found/not-found URLs

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

1. Create a `urls.txt` file with target URLs (one per line):

```
https://fastapi.tiangolo.com
https://docs.pydantic.dev
https://langchain.com
```

2. Run the audit:

```bash
uv run readability-auditor --input urls.txt --output-dir ./results
```

3. Check the results:
   - `results/results.csv` — Raw data with all metrics
   - `results/report.md` — Formatted summary with comparison tables

## CLI Options

```bash
uv run readability-auditor --help

Options:
  -i, --input PATH              Path to URLs file [default: urls.txt]
  -o, --output-dir PATH         Directory to save results [default: ./results]
  -d, --max-depth INT           Max depth for crawling docs (1-5) [default: 2]
  -p, --max-pages INT           Max pages to crawl per URL (1-50) [default: 10]
  --follow-links/--no-follow-links  Follow .txt links in llms.txt [default: follow-links]
  --use-context7/--no-context7  Use Context7 API as fallback [default: use-context7]
  -v, --verbose                 Enable verbose logging
  --help                        Show this message and exit
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

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **Flesch Reading Ease (FRE)** | Higher = easier to read. 90-100 = very easy, 0-30 = very difficult |
| **Flesch-Kincaid Grade (FK)** | US school grade level needed to understand the text |
| **Lexical Density (LD)** | Percentage of content words (nouns, verbs, adjectives, adverbs) |
| **Token-to-Word Ratio (T/W)** | AI tokenization efficiency. Lower = more efficient for LLMs |

## Research Context

This tool supports academic research on the "Paradox of Readability" — the linguistic shift from human-readable to machine-optimized documentation in the AI era.

## License

MIT
