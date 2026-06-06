# CODHES 2026 Research Plan: Python-Based Documentation Readability Analysis

**Researcher:** Yehezkiel Gunawan  
**Current Date:** 2026-06-06  
**Deadline:** 2026-06-15 (Phase 1) — 9 days remaining  
**Status:** Base experiment complete, LLM-as-a-Judge evaluation planned

---

## Executive Summary

**Current State:** The Python CLI tool (`readability-python-demo`) is fully functional with 11 tests passing. Base data collection completed across 10 technical documentation platforms. Text cleaning pipeline implemented for fair prose comparison. Ready to add LLM-as-a-Judge evaluation phase.

**Goal:** Complete LLM-as-a-Judge semantic evaluation, analyze all data, write the full paper, and submit within 9 days.

**Scope:** Technical documentation only (frameworks, libraries, platforms, developer tools) — excludes marketing sites, blogs, and non-technical content.

**Confidence Level:** High. Base experiment done; LLM evaluation and writing remain.

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

**Commands:**
```bash
cd readability-python-demo
uv run readability-auditor --input urls.txt --output-dir ./results
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

## Planned: LLM-as-a-Judge Evaluation (June 7)

**Rationale:** Traditional readability metrics (FRE, FKGL) were designed for human prose and may not fully capture the quality of machine-optimized documentation. Using an LLM to evaluate LLM-optimized text provides a "machine reviewer for machine docs" approach that is methodologically sound and novel.

**Model:** `nvidia/nemotron-3.5-content-safety:free` via OpenRouter
- Free tier available
- Content safety and quality evaluation capabilities
- Suitable for semantic analysis of technical documentation

**Evaluation Dimensions:**
1. **Clarity** — Is the documentation clear and unambiguous?
2. **Completeness** — Does it cover the topic adequately?
3. **Conciseness** — Is it free of unnecessary verbosity?
4. **Technical Accuracy** — Are technical details correct?
5. **LLM-Friendliness** — Is it optimized for machine consumption?

**Implementation Plan:**
- [ ] Set up OpenRouter API client
- [ ] Design evaluation prompts for each dimension
- [ ] Run evaluation on both human and machine text corpora
- [ ] Compare LLM scores between human docs and `llms.txt`
- [ ] Correlate LLM scores with traditional metrics (FRE, FKGL)

**Expected Outcome:**
- Quantitative LLM-based readability scores
- Correlation analysis: Do traditional metrics align with LLM judgment?
- Novel contribution: First study to use LLM-as-a-Judge for documentation readability

---

## Day-by-Day Plan

### Day 1: Data Collection (June 6) ✅ COMPLETE

**Status:** Base experiment complete. 10 platforms analyzed, raw data collected.

---

### Day 2: LLM-as-a-Judge Evaluation (June 7)

**Morning (2-3 hours):**

- [ ] Set up OpenRouter API client in Python
- [ ] Design evaluation prompts for 5 dimensions
- [ ] Test prompts on sample documentation
- [ ] Validate output format

**Afternoon (2-3 hours):**

- [ ] Run LLM evaluation on all 10 platforms
- [ ] Evaluate both human docs and `llms.txt` for each platform
- [ ] Collect and organize LLM scores
- [ ] Handle any API errors or retries

**Evening (1 hour):**

- [ ] Export LLM evaluation results to CSV
- [ ] Preliminary comparison: human vs machine LLM scores
- [ ] Document methodology for paper

**Deliverable:** LLM evaluation complete for all 10 platforms

---

### Day 3: Deep Statistical Analysis (June 8)

**Morning (2-3 hours):**

- [ ] Merge traditional metrics with LLM scores
- [ ] Paired comparison: HTML docs vs `llm.txt` (FRE, FKGL, LLM scores)
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

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| **Some platforms lack llm.txt** | Medium | High | Have 3 backup platforms ready (Next.js, Postman, Mintlify) |
| **LaTeX compilation errors** | Low | Medium | Test compilation daily; use Overleaf as fallback |
| **Word count short** | Medium | High | Expand discussion section; add examples |
| **Statistical significance weak** | Medium | Medium | Report as exploratory; focus on effect sizes |
| **Writing fatigue** | High | Medium | Write in 2-hour blocks; take breaks |
| **Turnitin similarity high** | Low | High | Check early; paraphrase if needed |
| **OpenRouter API issues** | Low | Medium | Have backup model ready; cache responses |
| **LLM evaluation bias** | Medium | Medium | Use multiple dimensions; report limitations |

---

## Daily Writing Target

| Day | Section | Target Words | Cumulative |
|-----|---------|-------------|------------|
| 1 | — | — | — |
| 2 | — | — | — |
| 3 | — | — | — |
| 4 | Intro + Related Work | 2,500 | 2,500 |
| 5 | Methodology | 2,000 | 4,500 |
| 6 | Results | 2,500 | 7,000 |
| 7 | Discussion + Conclusion | 2,000 | 9,000 |
| 8 | Polish | — | 9,000+ |
| 9 | Submit | — | 9,000+ |

**Average daily writing:** 2,000 words (manageable in 4-5 hours)

---

## Tools Ready

- **Analysis:** `readability-python-demo` CLI (Python + uv)
- **LLM Evaluation:** OpenRouter API (`nvidia/nemotron-3.5-content-safety:free`)
- **Writing:** LaTeX template (`codhes2026_template.tex`)
- **Charts:** Python matplotlib or seaborn
- **Stats:** Python scipy (t-test, correlation)
- **Citation:** Zotero or Mendeley (if needed)

---

## Success Metrics

- [x] 10 technical documentation pairs collected and analyzed
- [x] 11 tests passing (current: ✅ 11/11)
- [ ] LLM-as-a-Judge evaluation complete for all 10 platforms
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
3. We have 9 days
4. The data is public and accessible
5. The analysis is automated
6. The paper structure is clear (6 sections)

**Why this matters:**

- First academic study on `llm.txt` readability in technical documentation
- Novel contribution to technolinguistics
- **Novel methodology:** LLM-as-a-Judge for documentation evaluation
- Direct impact on technical writing practices
- Conference presentation opportunity

---

**Let's do this. 🚀**
