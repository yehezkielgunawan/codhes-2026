# AGENTS.md — readibility-demo

## Commands

| Command            | Purpose                                  |
| ------------------ | ---------------------------------------- |
| `pnpm dev`         | Start Vite dev server                    |
| `pnpm build`       | Build client + SSR bundles               |
| `pnpm test`        | Run Vitest (single run)                  |
| `pnpm test:watch`  | Run Vitest in watch mode                 |
| `pnpm check`       | Biome lint + format check (CI uses this) |
| `pnpm check:write` | Biome check + auto-fix                   |
| `pnpm format`      | Biome format only (auto-fix)             |
| `pnpm deploy`      | Build + deploy to Cloudflare Workers     |
| `pnpm cf-typegen`  | Regenerate Cloudflare Bindings types     |

Run order before committing: `pnpm check` → `pnpm test` → `pnpm build`

## Architecture

- **Runtime:** Hono on Cloudflare Workers (SSR)
- **JSX:** Hono JSX (`jsxImportSource: "hono/jsx"` in tsconfig) — **not React**. Do not use React imports or hooks.
- **Build:** Vite with `@cloudflare/vite-plugin` + `@tailwindcss/vite` + `vite-ssr-components`
- **Styling:** Tailwind CSS v4 — CSS-first config via `@import "tailwindcss"` in `src/style.css`. No `tailwind.config.js`.
- **Linting/Formatting:** Biome (tab indent, 80 char line width, double quotes, semicolons)
- **Testing:** Vitest — test files co-located as `*.test.ts`
- **Persistence:** IndexedDB (browser-side) — Cloudflare Worker is stateless

### Application Flow

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────┐
│   Browser       │ ──►  │  Cloudflare      │ ──►  │  External   │
│  (IndexedDB)    │      │  Worker (Hono)   │      │  Websites   │
│                 │ ◄──  │                  │ ◄──  │             │
└─────────────────┘      └──────────────────┘      └─────────────┘
```

1. User enters up to 10 documentation URLs in the web UI
2. Click **"Scrape Documentation"** → Worker fetches HTML + auto-detects `llms.txt`
3. Click **"Analyze"** → Worker compares readability (FRE, FKGL) and token efficiency
4. Results saved to IndexedDB (survives page refresh)

### Key Files

| File                          | Role                                                                         |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `src/index.tsx`               | App entry — Hono routes + page composition                                   |
| `src/renderer.tsx`            | HTML shell — `<ViteClient />` and `<Link />` from `vite-ssr-components/hono` |
| `src/style.css`               | Global styles + Tailwind import                                              |
| `src/routes/api.ts`           | API routes: `/api/scrape`, `/api/analyze`, `/api/health`                     |
| `src/lib/analysis.ts`         | Text analysis: FRE, FKGL, Gunning Fog, token count (cl100k_base), lexical density |
| `src/lib/scraper.ts`          | URL fetching + cheerio content extraction (removes nav/footer/ads)          |
| `src/lib/db.ts`               | IndexedDB wrapper for browser persistence                                    |
| `src/components/UrlForm.tsx`  | Dynamic URL input form (max 10)                                              |
| `src/components/ProgressBar.tsx` | Scraping/analysis progress indicator                                      |
| `src/components/ResultsTable.tsx` | Analysis results display                                                 |
| `src/client/app.ts`           | Client-side interactivity — API calls, IndexedDB, DOM updates                |
| `wrangler.jsonc`              | Cloudflare Workers config                                                    |
| `vite.config.ts`              | Vite plugins (cloudflare + tailwind + ssr)                                   |

### API Endpoints

| Endpoint         | Method | Request Body                    | Response                          |
| ---------------- | ------ | ------------------------------- | --------------------------------- |
| `/api/scrape`    | POST   | `{ urls: string[] }` (max 10)   | `{ results: ScrapedData[] }`      |
| `/api/analyze`   | POST   | `{ htmlText, llmText }`         | `{ result: ComparisonResult }`    |
| `/api/health`    | GET    | —                               | `{ status: "ok", timestamp }`     |

### Key Libraries

| Library           | Purpose                                    |
| ----------------- | ------------------------------------------ |
| `hono`            | Web framework (Cloudflare Workers)         |
| `cheerio`         | HTML parsing + content extraction          |
| `text-readability`| Readability metrics (FRE, FKGL, etc.)      |
| `js-tiktoken`     | BPE token counting (cl100k_base encoding)  |
| `tailwindcss`     | Utility-first CSS framework                |

## CI/CD

This project lives inside the `codhes-2026` monorepo. Workflows are at the repo root:

- **CI** (`.github/workflows/readibility-demo-ci.yml`): Runs `pnpm check` and `pnpm test` on push to `main` and PRs, scoped to `readibility-demo/**` changes.
- **CD** (`.github/workflows/readibility-demo-deploy.yml`): **Manual trigger only** (`workflow_dispatch`). Deploys to Cloudflare Workers. Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets.

## Conventions

- Tab indentation (enforced by Biome)
- Always utilize JSX components for UI, since Hono already has its built-in JSX (no manual DOM manipulation)
- Always run `pnpm check:write` before committing to auto-fix formatting
- Test Hono routes via `app.request()` — no need for a running server
- Use `CloudflareBindings` type (from `pnpm cf-typegen`) when accessing Worker bindings

## Available MCPs

Use these MCPs when relevant — prefer them over guessing or manual lookups:

| MCP                                                                 | Use For                                                                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Context7** (`context7_resolve-library-id`, `context7_query-docs`) | Look up docs, API references, and code examples for libraries (Hono, Tailwind, Vitest, Wrangler, etc.) |
| **GitHub** (`github-mcp-server_*`)                                  | GitHub API operations: PRs, issues, repos, actions, code search                                        |
| **Serena** (`serena_*`)                                             | Code analysis, symbol navigation, find references/declarations, refactoring, project-aware edits       |
