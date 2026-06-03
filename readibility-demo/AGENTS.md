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
- **Build:** Vite with `@cloudflare/vite-plugin` + `vite-ssr-components`
- **Styling:** Tailwind CSS v4 — CSS-first config via `@import "tailwindcss"` in `src/style.css`. No `tailwind.config.js`.
- **Linting/Formatting:** Biome (tab indent, 80 char line width, double quotes, semicolons)
- **Testing:** Vitest — test files co-located as `*.test.tsx`

### Key Files

| File               | Role                                                                         |
| ------------------ | ---------------------------------------------------------------------------- |
| `src/index.tsx`    | App entry — Hono routes                                                      |
| `src/renderer.tsx` | HTML shell — `<ViteClient />` and `<Link />` from `vite-ssr-components/hono` |
| `src/style.css`    | Global styles + Tailwind import                                              |
| `wrangler.jsonc`   | Cloudflare Workers config                                                    |
| `vite.config.ts`   | Vite plugins (cloudflare + ssr)                                              |

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
