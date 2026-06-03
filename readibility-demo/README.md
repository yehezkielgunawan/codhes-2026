# Readability & Token Efficiency Analyzer

A web application that compares HTML documentation vs `llm.txt` files for readability metrics and token efficiency. Built for the CODHES 2026 conference paper.

## Features

- **Auto-detect llm.txt**: Enter a documentation URL, we'll automatically find the `llms.txt` file
- **Readability Analysis**: Flesch Reading Ease, Flesch-Kincaid Grade Level, Gunning Fog Index
- **Token Efficiency**: BPE token counting using cl100k_base encoding (GPT-4/Claude compatible)
- **Lexical Density**: Content word ratio analysis
- **IndexedDB Persistence**: Results saved locally in your browser — survives page refresh
- **Progress Tracking**: Visual progress bar during scraping and analysis
- **Max 10 URLs**: Compare up to 10 documentation sites at once

## Getting Started

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Open browser
# http://localhost:5173
```

## How to Use

1. **Enter URLs**: Add up to 10 documentation URLs (e.g., `https://fastapi.tiangolo.com/`)
2. **Click "Scrape Documentation"**: We'll fetch HTML and auto-detect `llms.txt` files
3. **Click "Analyze"**: Compare readability and token efficiency
4. **View Results**: See comparison tables with metrics and summary cards

Results are automatically saved to IndexedDB and persist across page refreshes.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Hono | Web framework (Cloudflare Workers) |
| Tailwind CSS v4 | Utility-first styling |
| cheerio | HTML parsing + content extraction |
| text-readability | Readability metrics (FRE, FKGL, etc.) |
| js-tiktoken | BPE token counting (cl100k_base) |
| IndexedDB | Browser-side persistence |
| Vite | Build tool |
| Vitest | Testing |
| Biome | Linting + formatting |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scrape` | POST | Fetch HTML + llm.txt from URLs |
| `/api/analyze` | POST | Compare two text versions |
| `/api/health` | GET | Health check |

## Commands

```bash
pnpm dev          # Start dev server
pnpm build        # Build for production
pnpm test         # Run tests
pnpm check        # Lint + format check
pnpm check:write  # Auto-fix formatting
pnpm deploy       # Deploy to Cloudflare Workers
```

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────┐
│   Browser       │ ──►  │  Cloudflare      │ ──►  │  External   │
│  (IndexedDB)    │      │  Worker (Hono)   │      │  Websites   │
│                 │ ◄──  │                  │ ◄──  │             │
└─────────────────┘      └──────────────────┘      └─────────────┘
```

- **Stateless Worker**: Cloudflare Worker handles scraping and analysis only
- **Smart Browser**: Manages UI state, IndexedDB persistence, progress tracking

## Project Structure

```
src/
├── lib/
│   ├── analysis.ts    # Readability + token analysis
│   ├── scraper.ts     # URL fetching + content extraction
│   └── db.ts          # IndexedDB wrapper
├── routes/
│   └── api.ts         # API endpoints
├── components/
│   ├── UrlForm.tsx    # URL input form
│   ├── ProgressBar.tsx
│   └── ResultsTable.tsx
├── client/
│   └── app.ts         # Client-side interactivity
├── index.tsx          # Main app entry
├── renderer.tsx       # HTML shell
└── style.css          # Tailwind import
```

## License

MIT
