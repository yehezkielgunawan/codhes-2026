# CODHES 2026 Research Plan: Python-Based Documentation Readability Analysis

**Researcher:** Yehezkiel Gunawan  
**Current Date:** 2026-06-08
**Deadline:** 2026-06-15 (Phase 1) — 7 days remaining
**Status:** Day 3 — LLM evaluation COMPLETE for all 10 platforms; entering statistical analysis phase

---

## Executive Summary

**Current State:** The Python CLI tool (`readability-python-demo`) is fully functional with **50 tests passing**. Base data collection completed across 10 technical documentation platforms. LLM-as-a-Judge evaluation **COMPLETE** for all 10 platforms using OpenRouter API with 5-dimension Likert scale assessment and LLM Readability Index (LRI) calculation. Cached batch processing enabled fault-tolerant resumption after initial rate limiting.

**Goal:** Complete deep statistical analysis, create publication-ready charts, write the full paper, and submit within 7 days.

**Scope:** Technical documentation only (frameworks, libraries, platforms, developer tools) — excludes marketing sites, blogs, and non-technical content.

**Confidence Level:** High. Tool implementation done; experiment execution and writing remain.

---

## Tool: readability-python-demo

**Location:** `readability-python-demo/`
**Tech Stack:** Python 3.11+, `uv`, Typer, Crawl4AI, textstat, tiktoken, nltk, httpx, rich
**Entry Point:** `uv run readability-auditor --input urls.txt --output-dir ./results`

**Key Features:**

- Detects `llm.txt` / `llms.txt` with `[FOUND]` / `[NOT FOUND]` logging
- Deep crawling: BFS multi-page crawl (`--max-depth`, `--max-pages`)
- Linked `.txt` aggregation: follows links in `llms.txt` to fetch full content
- Context7 API fallback with length comparison
- Prose extraction: strips code blocks, navigation, images for fair comparison
- Dual export: CSV + Markdown + raw text files (`results/raw_texts/`)
- Metrics: Flesch Reading Ease, Flesch-Kincaid Grade, Lexical Density, Token-to-Word Ratio
- **LLM-as-a-Judge evaluation:** 5-dimension Likert scale assessment via OpenRouter API
- **LLM Readability Index (LRI):** Quantifies LLM scores on 0-100 scale for comparison with FRE
- **Resumable evaluation:** Caches API responses for fault-tolerant batch processing

**Commands:**

```bash
cd readability-python-demo

# Basic audit (traditional metrics only)
uv run readability-auditor --input urls.txt --output-dir ./results

# LLM evaluation during scraping
uv run readability-auditor --input urls.txt --output-dir ./results --evaluate-llm

# LLM evaluation on existing raw_texts (skip scraping)
uv run readability-auditor --output-dir ./results --evaluate-only

# Run tests
uv run pytest tests/ -v
```

---

## Completed: Base Experiment (June 6)

- [x] Python CLI tool implemented and tested (11 tests passing)
- [x] Text cleaning pipeline for fair prose extraction
- [x] Context7 API integration with fallback logic
- [x] Data collection from 10 technical documentation platforms
- [x] Raw data exported to `results/raw_texts/`
- [x] Initial metrics calculated (FRE, FKGL, LD, T/W)

**Platforms Analyzed:**

1. React (https://react.dev)
2. GitHub Docs (https://docs.github.com)
3. Supabase (https://supabase.com/docs)
4. Vercel (https://vercel.com/docs)
5. Stripe (https://stripe.com/docs)
6. LangChain (https://docs.langchain.com)
7. Cloudflare (https://developers.cloudflare.com)
8. Hono (https://hono.dev/docs)
9. FastAPI (https://fastapi.tiangolo.com)
10. Cursor (https://docs.cursor.com)

---

## Day 2: LLM-as-a-Judge Implementation (June 7)

### Coding Phase ✅ COMPLETE

- [x] Set up OpenRouter API client in Python (`llm_evaluator.py`)
- [x] Design evaluation prompts for 5 dimensions (`llm_prompts.py`)
- [x] Implement LLM Readability Index (LRI) calculation
- [x] Add `--evaluate-llm` flag for running evaluation during scraping
- [x] Add `--evaluate-only` flag for running evaluation on existing raw_texts
- [x] Implement text loader for reading from `results/raw_texts/`
- [x] Add caching mechanism for resumable batch processing
- [x] Implement retry logic with exponential backoff and rate limit handling
- [x] Export LLM evaluation results to `llm_evaluation.csv`
- [x] Update `report.md` to include LLM evaluation section
- [x] Write comprehensive tests (50 tests passing, up from 11)
- [x] Update README.md and AGENTS.md with new features

**Implementation Details:**

**Model:** `meta-llama/llama-3.2-3b-instruct:free` via OpenRouter
- Free tier available
- General-purpose LLM suitable for documentation evaluation
- Reliable JSON output format

**Evaluation Dimensions (1-5 Likert scale):**

1. **Clarity** — Is the documentation clear and unambiguous?
2. **Completeness** — Does it cover the topic adequately?
3. **Conciseness** — Is it free of unnecessary verbosity?
4. **Technical Accuracy** — Are technical details correct?
5. **LLM-Friendliness** — Is it optimized for machine consumption?

**Quantification Method:**

```
LRI = (Average of 5 dimensions - 1) / 4 × 100
```

Maps 1-5 Likert scale to 0-100 for direct comparison with Flesch Reading Ease:
- All 1s → 0/100
- All 3s → 50/100
- All 5s → 100/100

**New Modules:**

- `llm_evaluator.py` — Evaluation engine with chunking, API calls, caching
- `llm_prompts.py` — Prompt templates, JSON parsing, validation
- `text_loader.py` — Reads raw texts for evaluate-only mode

**Modified Modules:**

- `models.py` — Added `LLMScores` dataclass
- `cli.py` — Added `--evaluate-llm` and `--evaluate-only` flags
- `exporter.py` — Added LLM results export to CSV and Markdown

**Test Coverage:**

- 50 tests total (11 original + 39 new)
- Tests cover prompt building, JSON parsing, chunking, LRI calculation, text loading
- All tests passing

### Experiment Phase ✅ COMPLETE

**Status:** LLM evaluation successfully completed for all 10 platforms using cached batch processing.

**Results:**

- `results/llm_evaluation.csv` — LLM scores for all 5 dimensions across 20 document pairs (10 human + 10 machine)
- `results/llm_cache/` — 80 cached API responses enabling full reproducibility
- `results/report.md` — Updated with LLM evaluation section
- All platforms evaluated without data loss despite initial rate limiting

**Key Findings (Preliminary):**

| Platform | Human LRI | Machine LRI | Δ LRI |
|----------|-----------|-------------|-------|
| stripe.com | 55.0 | 80.0 | +25.0 |
| fastapi.tiangolo.com | 87.0 | 100.0 | +13.0 |
| hono.dev | 73.3 | 87.0 | +13.7 |
| docs.cursor.com | 75.0 | 100.0 | +25.0 |
| supabase.com | 56.0 | 82.0 | +26.0 |
| docs.github.com | 55.0 | 81.3 | +26.3 |
| vercel.com | 54.0 | 42.0 | -12.0 |
| developers.cloudflare.com | 63.0 | 80.0 | +17.0 |
| react.dev | 72.0 | 85.0 | +13.0 |
| docs.langchain.com | 50.0 | 50.0 | 0.0 |

**Mitigation Strategy (Executed):**

1. ✅ **Caching:** Skipped already-cached chunks on re-run, saving API calls and time
2. ✅ **Rate limit handling:** Tool automatically waited and retried on 429 errors
3. ✅ **Resumable pipeline:** Full evaluation completed with zero data loss

---

## Day-by-Day Plan

### Day 1: Data Collection (June 6) ✅ COMPLETE

**Status:** Base experiment complete. 10 platforms analyzed, raw data collected.

---

### Day 2: LLM-as-a-Judge Implementation (June 7) ✅ COMPLETE

**Coding Phase:** ✅ COMPLETE (all modules implemented, 50 tests passing)

**Experiment Phase:** ✅ COMPLETE (all 10 platforms evaluated, cached batch processing successful)

**Deliverable:** LLM evaluation complete for all 10 platforms

---

### Day 3: Deep Statistical Analysis (June 8) 🔄 IN PROGRESS

**Morning (2-3 hours):**

- [x] Merge traditional metrics with LLM scores
- [x] Paired comparison: HTML docs vs `llm.txt` (FRE, FKGL, LLM scores)
- [ ] Effect size calculation (Cohen's d)
- [ ] Pearson correlation: traditional metrics ↔ LLM scores
- [ ] Generate summary statistics table

**Afternoon (2-3 hours):**

- [ ] Create publication-ready charts
  - Bar chart: Readability comparison (FRE + LLM scores)
  - Bar chart: Token count comparison
  - Scatter plot: FRE vs LLM clarity score
  - Box plot: Distribution of differences
- [ ] Save charts as PNG/SVG to `paper/figures/`

**Evening (1 hour):**

- [ ] Write Results section outline
- [ ] Prepare tables for Results section
- [ ] Document findings in research notes

**Deliverable:** Statistical analysis complete + 4 charts ready

---

### Day 4: Paper Writing - Introduction + Related Work (June 9)

**Morning (3-4 hours):**

- [ ] Write Introduction (800-1000 words)
  - Background: HTML documentation bloat in technical docs
  - The emergence of `llm.txt` (Sept 2024)
  - Research gap: no readability comparison for technical documentation
  - Three Research Questions (RQ1-3)

**Afternoon (3-4 hours):**

- [ ] Write Related Work (1200-1500 words)
  - Readability metrics: Flesch (1948), Kincaid (1975)
  - Tokenization: BPE (Sennrich et al., 2016)
  - LLM context windows: "Lost in the Middle" (Liu et al., 2023)
  - Prompt compression: LLMLingua (Jiang et al., 2023)
  - LLM-as-a-Judge: recent work on using LLMs for evaluation
  - Documentation formats: plain text vs HTML for technical docs
  - Gap analysis: no study compares HTML vs `llm.txt` in technical documentation

**Evening (1 hour):**

- [ ] Compile and verify LaTeX builds
- [ ] Check word count progress
- [ ] Review citations

**Deliverable:** 2,000-2,500 words written

---

### Day 5: Paper Writing - Methodology (June 10)

**Morning (3-4 hours):**

- [ ] Write Methodology (1500-2000 words)
  - Research design: Paired comparison, quantitative content analysis
  - Corpus selection: 10 technical platforms, criteria
  - Data collection: Python CLI tool (`readability-python-demo`)
  - Text cleaning: prose extraction pipeline
  - Metrics: Table 2 (formulas, instruments)
  - LLM-as-a-Judge: OpenRouter model, evaluation dimensions, prompts

**Afternoon (2-3 hours):**

- [ ] Write Analysis Procedure
  - Statistical tests: paired comparison, effect sizes
  - Software: Python `textstat`, `tiktoken`, `nltk`
  - LLM evaluation: OpenRouter API, prompt design
  - Tool: `readability-python-demo` CLI
  - Validation steps

**Evening (1 hour):**

- [ ] Compile and verify
- [ ] Add methodology tables
- [ ] Review with advisor (if possible)

**Deliverable:** 3,500-4,500 words total

---

### Day 6: Paper Writing - Results (June 11)

**Morning (3-4 hours):**

- [ ] Write Results (2000-2500 words)
  - Descriptive statistics table
  - Readability comparison table (traditional + LLM scores)
  - Token efficiency table
  - Lexical density analysis
  - LLM-as-a-Judge evaluation results
  - Correlation: traditional metrics vs LLM scores
  - Statistical significance
  - Insert charts (Figure 1, 2, 3, 4)

**Afternoon (2-3 hours):**

- [ ] Write aggregate findings
- [ ] Create comparison tables
- [ ] Verify all charts display correctly
- [ ] Add figure captions

**Evening (1 hour):**

- [ ] Compile and verify
- [ ] Check word count: should be 5,500-7,000

**Deliverable:** Results section complete with all tables and charts

---

### Day 7: Paper Writing - Discussion + Conclusion (June 12)

**Morning (3-4 hours):**

- [ ] Write Discussion (1500-2000 words)
  - Interpretation: Why is `llm.txt` more token-efficient in technical docs?
  - LLM-as-a-Judge insights: Do machines prefer machine-optimized docs?
  - Implications for technical writers
  - Implications for LLM users
  - Limitations: small sample, English-only, technical docs only, LLM bias
  - Future work: expand to 50 platforms, Markdown comparison, user studies

**Afternoon (2-3 hours):**

- [ ] Write Conclusion (500-800 words)
  - Summarize key findings
  - Answer RQ1, RQ2, RQ3
  - Final statement

**Evening (1 hour):**

- [ ] Write Abstract (150-250 words)
- [ ] Write Keywords (5 terms)
- [ ] Compile and verify LaTeX

**Deliverable:** Full draft complete (8,000-10,000 words)

---

### Day 8: Polish and Quality Check (June 13)

**Morning (2-3 hours):**

- [ ] Spell check (aspell)
- [ ] Grammar check (Grammarly or similar)
- [ ] Verify all citations in IEEE format
- [ ] Check all figures/tables referenced in text
- [ ] Verify no placeholder text

**Afternoon (2-3 hours):**

- [ ] Run similarity check (Turnitin)
- [ ] Review with fresh eyes (or ask peer)
- [ ] Fix any compilation issues
- [ ] Generate final PDF

**Evening (1 hour):**

- [ ] Create submission package
- [ ] Prepare zip file (PDF + LaTeX source + figures)
- [ ] Verify file size < 10MB

**Deliverable:** Final PDF ready for submission

---

### Day 9: Submit (June 14)

**Morning (1-2 hours):**

- [ ] Log into CODHES CMT system
- [ ] Upload submission package
- [ ] Fill in metadata (title, authors, abstract, keywords)
- [ ] Select Track 14: Technolinguistics

**Afternoon (1 hour):**

- [ ] Verify submission received
- [ ] Save confirmation email
- [ ] Create git tag: `v1.0-submission`
- [ ] Push to GitHub

**Evening:**

- [ ] Celebrate! 🎉

**Deliverable:** Paper submitted to CODHES 2026

---

## Risk Mitigation

| Risk                              | Probability | Impact | Mitigation                                                 |
| --------------------------------- | ----------- | ------ | ---------------------------------------------------------- |
| **Some platforms lack llm.txt**   | Medium      | High   | Have 3 backup platforms ready (Next.js, Postman, Mintlify) |
| **LaTeX compilation errors**      | Low         | Medium | Test compilation daily; use Overleaf as fallback           |
| **Word count short**              | Medium      | High   | Expand discussion section; add examples                    |
| **Statistical significance weak** | Medium      | Medium | Report as exploratory; focus on effect sizes               |
| **Writing fatigue**               | High        | Medium | Write in 2-hour blocks; take breaks                        |
| **Turnitin similarity high**      | Low         | High   | Check early; paraphrase if needed                          |
| **OpenRouter API rate limits**    | High        | Medium | Cache responses, resume from checkpoint, consider paid tier|
| **LLM evaluation bias**           | Medium      | Medium | Use multiple dimensions; report limitations                |

---

## Daily Writing Target

| Day | Section                 | Target Words | Cumulative |
| --- | ----------------------- | ------------ | ---------- |
| 1   | —                       | —            | —          |
| 2   | —                       | —            | —          |
| 3   | —                       | —            | —          |
| 4   | Intro + Related Work    | 2,500        | 2,500      |
| 5   | Methodology             | 2,000        | 4,500      |
| 6   | Results                 | 2,500        | 7,000      |
| 7   | Discussion + Conclusion | 2,000        | 9,000      |
| 8   | Polish                  | —            | 9,000+     |
| 9   | Submit                  | —            | 9,000+     |

**Average daily writing:** 2,000 words (manageable in 4-5 hours)

---

## Tools Ready

- **Analysis:** `readability-python-demo` CLI (Python + uv)
- **LLM Evaluation:** OpenRouter API (`meta-llama/llama-3.2-3b-instruct:free`)
- **Writing:** LaTeX template (`codhes2026_template.tex`)
- **Charts:** Python matplotlib or seaborn
- **Stats:** Python scipy (t-test, correlation)
- **Citation:** Zotero or Mendeley (if needed)

---

## Success Metrics

- [x] 10 technical documentation pairs collected and analyzed
- [x] 50 tests passing (current: ✅ 50/50)
- [x] LLM-as-a-Judge evaluation module implemented
- [x] LLM evaluation complete for all 10 platforms (COMPLETED June 8)
- [ ] 8,000+ words in final paper
- [ ] All charts publication-ready
- [ ] Statistical analysis complete (traditional + LLM metrics)
- [ ] LaTeX compiles with 0 errors
- [ ] Turnitin similarity < 20%
- [ ] Submitted before June 15, 2026

---

## Motivation

**Why this is achievable:**

1. The hard part (tool building) is DONE
2. Base experiment is COMPLETE
3. LLM evaluation module is IMPLEMENTED
4. We have 7 days
5. The data is public and accessible
6. The analysis is automated
7. The paper structure is clear (6 sections)
8. **Caching ensures resumable evaluation** — no progress lost

**Why this matters:**

- First academic study on `llm.txt` readability in technical documentation
- Novel contribution to technolinguistics
- **Novel methodology:** LLM-as-a-Judge for documentation evaluation
- **Novel quantification:** LLM Readability Index (LRI) for comparing LLM scores with traditional metrics
- Direct impact on technical writing practices
- Conference presentation opportunity

---

**Let's do this. 🚀**
